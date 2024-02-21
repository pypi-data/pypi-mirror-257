import torch
import torch.nn as nn

class Encoder(nn.Module):

    def __init__(self, dim_input, dim_z, drop=0.2, complication=2):
        # dim_input is the dim of x, dim_z is the dim of means and variance of z
        super(Encoder, self).__init__()
        if complication == 0:
            dim1 = 32
        elif complication==1:
            dim1 = 64
        elif complication == 2:
            dim1 = 256
        elif complication == 3:
            dim1 = 512
        dim2 = dim1
        self.hidden1 = nn.Linear(dim_input, dim1)
        self.hidden2 = nn.Linear(dim1, dim2)
        self.out = nn.Linear(dim2, 2 * dim_z)
        self.tanh = nn.Tanh()
        self.lrelu = nn.LeakyReLU(0.1)
        self.drop=nn.Dropout(drop)

    def forward(self, x):
        x = self.lrelu(self.drop(self.hidden1(x)))
        x = self.lrelu(self.drop(self.hidden2(x)))
        return self.lrelu(self.out(x))


class Decoder(nn.Module):
    def __init__(self, dim_z, dim_x, drop=0.2, complication=2):
        super(Decoder, self).__init__()
        if complication == 0:
            dim1 = 32
        elif complication==1:
            dim1 = 64
        elif complication == 2:
            dim1 = 256
        elif complication == 3:
            dim1 = 512
        dim2 = dim1
        self.hidden1 = nn.Linear(dim_z, dim1)
        self.hidden2 = nn.Linear(dim1, dim2)
        self.out = nn.Linear(dim2, 2 * dim_x)
        self.tanh = nn.Tanh()
        self.lrelu = nn.LeakyReLU(0.1)
        self.drop=nn.Dropout(drop)

    def forward(self, z):
        z = self.lrelu(self.drop(self.hidden1(z)))
        z = self.lrelu(self.drop(self.hidden2(z)))
        return self.lrelu(self.out(z)) 
    
    
class PriorCoder(nn.Module):
    def __init__(self, dim_u, dim_z, drop=0.2, complication=2):
        super(PriorCoder, self).__init__()
        if complication == 0:
            dim1 = 32
        elif complication==1:
            dim1 = 64
        elif complication == 2:
            dim1 = 256
        elif complication == 3:
            dim1 = 512
        dim2 = dim1
        self.hidden1 = nn.Linear(dim_u, dim1)
        self.hidden2 = nn.Linear(dim1, dim2)
        self.out = nn.Linear(dim2, 2 * dim_z)
        self.tanh = nn.Tanh()
        self.lrelu = nn.LeakyReLU(0.1)
        self.drop=nn.Dropout(drop)
        
    def forward(self, u):
        u = self.lrelu(self.drop(self.hidden1(u)))
        u = self.lrelu(self.drop(self.hidden2(u)))
        return self.lrelu(self.out(u))
    
    
class PredictNetwork(nn.Module):
    def __init__(self, dim_input, drop=0.2, complication=2):
        super(PredictNetwork, self).__init__()
        if complication == 0:
            dim1 = 32
        elif complication==1:
            dim1 = 64
        elif complication == 2:
            dim1 = 256
        elif complication == 3:
            dim1 = 512
        dim2 = dim1
        self.hidden1 = nn.Linear(dim_input, dim1)
        self.hidden2 = nn.Linear(dim1, dim2)
        self.out = nn.Linear(dim2, 2)
        self.tanh = nn.Tanh()
        self.lrelu = nn.LeakyReLU(0.1)
        self.drop=nn.Dropout(drop)
        
    def forward(self, x):
        x = self.lrelu(self.drop(self.hidden1(x)))
        x = self.lrelu(self.drop(self.hidden2(x)))
        return self.lrelu(self.out(x))
        


class LASER(nn.Module):

    def __init__(self, dim_x, dim_m, dim_z, drop=0.2, complication=2):
        """
        x: covariate
        m: observable proxies
        z: latent variables
        """
        super(LASER, self).__init__()
        self.dim_x, self.dim_z, self.dim_m = dim_x, dim_z, dim_m
        self.encoder = Encoder(dim_x + dim_m + 1, dim_z, drop, complication=complication)
        self.decoder = Decoder(dim_z, dim_m, drop, complication=complication)
        self.priorcoder = PriorCoder(dim_x + 1, dim_z, drop, complication=complication)
        self.predictor = PredictNetwork(dim_x + dim_z, drop, complication=complication)

    def forward(self, x, t, m):
        # x.shape = batch_size, dim_x, u.shape = batch_size, dim_u
        # output: encoder output, decoder output, prior coder output, prediction output
        batch_size, _ = x.shape
        
        xtm = torch.cat([x, t, m], dim=1)
        out_encoder = self.encoder(xtm)  # out_encoder.shape = batch_size, 2 * dim_z
        # here, L = 1 by default
        e = torch.randn(size=(batch_size, self.dim_z)).to(x.device)
        mu = out_encoder[:, :self.dim_z]
        sigma = torch.exp(out_encoder[:, self.dim_z:])
        encoded_z = sigma * e + mu # [sigma2, mu]
        
        out_decoder = self.decoder(encoded_z)
        
        xt = torch.cat([x, t], dim=1)
        prior_coder = self.priorcoder(xt)
        
        sxt = torch.cat([encoded_z, x], dim=1)
        out_predictor = self.predictor(sxt)
        
        return out_encoder, out_decoder, prior_coder, out_predictor
    
    @torch.no_grad()
    def predict(self, x, t, m):
        batch_size, _ = x.shape
        
        xtm = torch.cat([x, t, m], dim=1)
        out_encoder = self.encoder(xtm)  # out_encoder.shape = batch_size, 2 * dim_z
        # here, L = 1 by default
        e = torch.randn(size=(batch_size, self.dim_z)).to(x.device)
        mu = out_encoder[:, :self.dim_z]
        sigma = torch.exp(out_encoder[:, self.dim_z:])
        encoded_z = sigma * e + mu # [sigma2, mu]

        sx = torch.cat([encoded_z, x], dim=1)
        out_predictor = self.predictor(sx)
        
        return out_predictor[:, :1]
    
# https://github.com/siamakz/iVAE/blob/master/lib/models.py
