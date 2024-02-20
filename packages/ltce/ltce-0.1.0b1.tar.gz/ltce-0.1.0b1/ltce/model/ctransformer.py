import torch
import torch.nn as nn
import numpy as np


class MultiheadAttLayer(nn.Module):
    def __init__(self, input_dim, n_heads, dim_k, dim_v, temp, drop=0.1, atten_drop=0.1):
        super(MultiheadAttLayer, self).__init__()
        self.n_heads = n_heads
        self.dim_k = dim_k 
        self.dim_v = dim_v
        self.attention_q = nn.Linear(input_dim, n_heads * dim_k)
        self.attention_k = nn.Linear(input_dim, n_heads * dim_k)
        self.attention_v = nn.Linear(input_dim, n_heads * dim_v)
        self.attdrop = nn.Dropout(atten_drop)
        self.drop = nn.Dropout(drop)
        self.temp = temp
        self.fc = nn.Linear(n_heads * dim_v, input_dim)
        self.layer_norm = nn.LayerNorm(input_dim, eps=1e-6)
        
        nn.init.xavier_uniform_(self.attention_q.weight)
        nn.init.xavier_uniform_(self.attention_k.weight)
        nn.init.xavier_uniform_(self.attention_v.weight)
        nn.init.xavier_uniform_(self.fc.weight)
        
    def forward(self, q, k, v, mask=None):
        # x shape: batch_size, max_len, input_dim
        # mask: batch_size, max_len, max_len
        batch_size, length_q, _ = q.shape
        length_k, length_v = k.shape[1], v.shape[1]
        res = q
        # 获得q、k、v
        q = self.attention_q(q).view(batch_size, length_q, self.n_heads, self.dim_k)
        k = self.attention_k(k).view(batch_size, length_k, self.n_heads, self.dim_k)
        v = self.attention_v(v).view(batch_size, length_v, self.n_heads, self.dim_v) # length_k = length_v !
        
        q, k, v = q.transpose(1, 2), k.transpose(1, 2), v.transpose(1, 2)
        
        # attention dot
        att = torch.matmul(q / self.temp, k.transpose(2,3)) # batch_size, n_heads, length_q, length_k
        if mask is not None:
            att = att.masked_fill(mask.unsqueeze(1)==0, -1e9)
        att = nn.Softmax(dim=-1)(att)  # batch_size, n_head, length_q, length_k; 
        v = torch.matmul(self.attdrop(att), v) # batch_size, n_head, length_q, dim_v
        v = self.drop(self.fc(v.transpose(1, 2).contiguous().view(batch_size, length_q, -1))) + res # residual connection
        v = self.layer_norm(v)
        
        return v, att
    
class FeedForwardLayer(nn.Module):
    def __init__(self, input_dim, hidden_dim, drop=0.1):
        super(FeedForwardLayer, self).__init__()
        self.input_dim = input_dim
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, input_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(drop)
        self.layer_norm = nn.LayerNorm(input_dim)
        
    def forward(self, x):
        y = self.dropout(self.layer2(self.relu(self.layer1(x))))
        y = y + x
        y = self.layer_norm(y)
        return y

class EncoderLayer(nn.Module):
    def __init__(self, input_dim, dim_k, dim_v, dim_hidden, n_head, drop=0.1, att_drop=0.1):
        super(EncoderLayer, self).__init__()
        
        self.multilayer1 = MultiheadAttLayer(input_dim, n_head, dim_k, dim_v, dim_k ** 0.5, drop, att_drop)
        self.feedlayer1 = FeedForwardLayer(input_dim, dim_hidden)
        
    def forward(self, x, mask=None):
        x, att = self.multilayer1(x, x, x, mask)
        x = self.feedlayer1(x)
        return x, att
    
class DecoderLayer(nn.Module):
    def __init__(self, input_dim, dim_k, dim_v, dim_hidden, n_head, drop=0.1, att_drop=0.1):
        super(DecoderLayer, self).__init__()
        self.multilayer1 = MultiheadAttLayer(input_dim, n_head, dim_k, dim_v, dim_k ** 0.5, drop, att_drop)
        self.multilayer2 = MultiheadAttLayer(input_dim, n_head, dim_k, dim_v, dim_k ** 0.5, drop, att_drop)
        self.feedlayer1 = FeedForwardLayer(input_dim, dim_hidden)
        
    def forward(self, x, enc_x, mask_x=None, mask_enc=None):
        x, att1 = self.multilayer1(x, x, x, mask_x)
        x, att2 = self.multilayer2(x, enc_x, enc_x, mask_enc)
        x = self.feedlayer1(x)
        return x, att1, att2
    
class PositionalEncoding(nn.Module):
    def __init__(self, dim_model, n_pos):
        super(PositionalEncoding, self).__init__()
        self.dim_model = dim_model
        self.n_pos = n_pos
        pos = [[p / 10000 ** (2 * (i // 2) / dim_model) for i in range(dim_model)] for p in range(n_pos)]
        pos = np.asarray(pos)
        pos[:, 0::2] = np.sin(pos[:, 0::2])
        pos[:, 1::2] = np.cos(pos[:, 1::2])
        pos = torch.FloatTensor(pos).unsqueeze(0)
        self.register_buffer('pos_table', pos)
    
    def forward(self, x):
        # x shape: batch_size, n_pos, dim_model
        # print(x.shape, self.pos_table.shape)

        return x + self.pos_table[:, :x.shape[1], :].clone().detach()
    
# class Predictor(nn.Module):
#     def __init__(self, dim_input, drop=0.1):
#         super(Predictor, self).__init__()
#         self.l1 = nn.Linear(dim_input, 256) # 原参数是 512， 256
#         self.l2 = nn.Linear(256, 128)
#         self.l3 = nn.Linear(128, 1)
#         self.relu = nn.ReLU()
#         self.dropout = nn.Dropout(drop)
        
#     def forward(self, x):
#         x = self.relu(self.dropout(self.l1(x)))
#         x = self.relu(self.dropout(self.l2(x)))
#         return self.l3(x)
    
class Predictor(nn.Module):
    def __init__(self, dim_input, drop=0.1):
        super(Predictor, self).__init__()
        self.l1 = nn.Linear(dim_input, dim_input)
        # self.l2 = nn.Linear(512, 256)
        self.l3 = nn.Linear(dim_input, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(drop)
        self.layer_norm = nn.LayerNorm(dim_input)
        
    def forward(self, x):
        # x = self.relu(self.dropout(self.l1(x))) + x
        # x = self.layer_norm(x)
        return self.l3(x)
    
def mask_padding(seq, pad_idx):
    return (seq !=pad_idx).unsqueeze(-2)

def mask_subsequent(seq):
    l = seq.shape[1]
    subsequent_mask = (1 - torch.triu(torch.ones((1, l, l), device=seq.device), diagonal=1)).bool()
    return subsequent_mask

class PositionalEmbedding(nn.Module):
    def __init__(self, dim_model, n_pos):
        super(PositionalEmbedding, self).__init__()
        self.dim_model = dim_model
        self.n_pos = n_pos
        self.embedding = nn.Embedding(n_pos, dim_model)
    
    def forward(self, x):
        # x shape: batch_size, n_pos, dim_model
        # print(x.shape, self.pos_table.shape)
        pos = torch.arange(x.shape[1]).long().unsqueeze(0).repeat(x.shape[0], 1).to(x.device)

        return x + self.embedding(pos)

class Encoder(nn.Module):
    def __init__(self, dim_input, dim_embedding, n_layers, n_heads, dim_k, dim_v, dim_hidden, n_pos=200, drop=0.1, learned_pos=False):
        super(Encoder, self).__init__()
        self.n_layers = n_layers
        self.embedding = nn.Linear(dim_input, dim_embedding)
        if learned_pos:
            self.pos_encoding = PositionalEmbedding(dim_embedding, n_pos)
        else:
            self.pos_encoding = PositionalEncoding(dim_embedding, n_pos)
        self.dropout = nn.Dropout(drop)
        self.layerstack = nn.ModuleList([EncoderLayer(dim_embedding, dim_k ,dim_v, dim_hidden, n_heads, drop, drop) for _ in range(n_layers)])
        self.layer_norm = nn.LayerNorm(dim_embedding)
        
    def forward(self, x, mask=None, return_emb_x=False):
        emb_x = self.embedding(x)
        x = self.dropout(self.pos_encoding(emb_x))
        # x = self.dropout(emb_x)
        x = self.layer_norm(x)
        
        all_att = []
        
        for enc_layer in self.layerstack:
            x, att = enc_layer(x, mask)
            # if return_att:
            #     all_att += [att]
        
        if not return_emb_x:
            return x
        else:
            return x, emb_x

class Decoder(nn.Module):
    def __init__(self, dim_output, dim_embedding, n_layers, n_heads, dim_k, dim_v, dim_hidden, n_pos=200, drop=0.1, learned_pos=False):
        super(Decoder, self).__init__()
        self.embedding = nn.Linear(dim_output, dim_embedding)
        if learned_pos:
            self.pos_encoding = PositionalEmbedding(dim_embedding, n_pos)
        else:
            self.pos_encoding = PositionalEncoding(dim_embedding, n_pos)
        self.dropout = nn.Dropout(drop)
        self.layerstack = nn.ModuleList([DecoderLayer(dim_embedding, dim_k, dim_v, dim_hidden, n_heads, drop, drop) for _ in range(n_layers)])
        self.layer_norm = nn.LayerNorm(dim_embedding)
        
    def forward(self, x, x_enc, mask_x=None, mask_enc=None, return_att=False):
        x = self.embedding(x)
        x = self.dropout(self.pos_encoding(x))
        x = self.layer_norm(x)
        all_att1, all_att2 = [], []
        for dec_layer in self.layerstack:
            x, att1, att2 = dec_layer(x, x_enc, mask_x, mask_enc)
            if return_att:
                all_att1 += [att1]
                all_att2 += [att2]
        if return_att:
            return x, all_att1, all_att2
        else:
            return x
        
        
class CPredictor(nn.Module):
    def __init__(self, dim_input, dim_class, drop=0.1):
        super(CPredictor, self).__init__()
        self.l1 = nn.Linear(dim_input, dim_input)
        # self.l2 = nn.Linear(512, 256)
        self.l3 = nn.Linear(dim_input, dim_class)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(drop)
        self.layer_norm = nn.LayerNorm(dim_input)
        
    def forward(self, x):
        x = self.relu(self.dropout(self.l1(x))) + x
        x = self.layer_norm(x)
        return self.l3(x)
    

class CTransformer(nn.Module):
    def __init__(self, dim_input, dim_output, dim_embedding, n_layers, n_heads, dim_k, dim_v, dim_hidden, dim_class, t0, drop=0.1, drop_pred=0.5, learned_pos=False, use_treat_in_pred=False):
        super(CTransformer, self).__init__()
        self.use_treat_in_pred = use_treat_in_pred
        self.encoder = Encoder(dim_input=dim_input, dim_embedding=dim_embedding, n_layers=n_layers, n_heads=n_heads, dim_k=dim_k, dim_v=dim_v, dim_hidden=dim_hidden, drop=drop, learned_pos=learned_pos)
        self.decoder = Decoder(dim_output=dim_output, dim_embedding=dim_embedding, n_layers=n_layers, n_heads=n_heads, dim_k=dim_k, dim_v=dim_v, dim_hidden=dim_hidden, drop=drop, learned_pos=learned_pos)
        if use_treat_in_pred:
            self.predictor = CPredictor(dim_embedding * t0 + t0, dim_class, drop=drop_pred)
        else:
            self.predictor = CPredictor(dim_embedding * t0, dim_class, drop=drop_pred)
        self.fc = nn.Linear(dim_embedding, dim_output)
    
    def forward(self, input_seq, output_seq, return_latent=False):
        dec_mask = mask_subsequent(output_seq)
        enc_out = self.encoder(input_seq)
        dec_out = self.decoder(output_seq, enc_out, dec_mask)
        if self.use_treat_in_pred:
            # long_input = torch.cat([enc_out, dec_out, input_seq[:, :, -1:]], dim=2)
            long_input = torch.cat([enc_out, input_seq[:, :, -1:]], dim=2)
        else:
            # long_input = torch.cat([enc_out, dec_out], dim=2)
            long_input = torch.cat([enc_out], dim=2)
        dec_out = self.fc(dec_out)
        
        long_out = self.predictor(long_input.view(long_input.shape[0], -1))
        if return_latent:
            return dec_out, long_out, enc_out
        return dec_out, long_out # batch_size, l, n_trg