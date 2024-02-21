import torch
import torch.nn as nn


class Wasserstein(nn.Module):
    def __init__(self, max_len, eps=1, its=100, device='cuda' if torch.cuda.is_available() else 'cpu'):
        super(Wasserstein, self).__init__()
        self.max_len = max_len
        self.eps = eps
        self.its = its
        self.device = device
        
    def _get_cost(self, xi, yi):
        # xi: batch_size, dim_x, yi: batch_size, dim_x
        cross = -2 * torch.matmul(xi, yi.T)
        xi2 = torch.sum(xi * xi, dim=1, keepdim=True)
        yi2 = torch.sum(yi * yi, dim=1, keepdim=True)
        return torch.sqrt(xi2 + yi2.T - cross)
    
    def forward(self, X, Y, eps=None, its=None):
        # X shape: nt, max_len, dim_rnn_output
        if eps is None:
            eps = self.eps
        if its is None:
            its = self.its
        nx, ny = X.shape[0], Y.shape[0]
        
        D = 0
        seq_len = X.shape[1]
        for i in range(min(seq_len, self.max_len)):
            C = self._get_cost(X[:, i, :], Y[:, i, :])
            with torch.no_grad():
                K = torch.exp(-C / eps) # batch_size_x, batch_size_y
                # cal a, b
                a = torch.ones([nx]).to(device) / nx
                b = torch.ones([ny]).to(device) / ny
                v = torch.ones([ny]).to(device)
                for _ in range(its):
                    u = a / torch.matmul(K, v)
                    v = b / torch.matmul(u.T, K)
            # print((K * v).shape)
            D += torch.mean(((K * v).T * u).T * C)
        return D
    
    
class MLP(nn.Module):
    def __init__(self, dim_input, dim_rnn_input):
        super(MLP, self).__init__()
        dim1 = 512 # 512
        dim2 = 2 * dim1
        self.l1 = nn.Linear(dim_input, dim1)
        self.l2 = nn.Linear(dim1, dim2)
        self.l3 = nn.Linear(dim2, dim_rnn_input)
        self.tanh = nn.Tanh()
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # x: batch_size, max_len, dim_input
        x = self.tanh(self.l1(x))
        x = self.tanh(self.l2(x))
        return self.relu(self.l3(x))

    
class LTEE(nn.Module):
    def __init__(self, MLP, dim_rnn_input, dim_rnn_output, dim_att, t0):
        # 原始尺寸，dim_input
        # GRU的输入尺寸，dim_rnn_input
        # GRU的输出尺寸，dim_rnn_out
        super(LTEE, self).__init__()
        self.mlp = MLP
        self.grut = nn.GRU(dim_rnn_input, dim_rnn_output, batch_first=True, bidirectional=True)  # 注意batch_first要设置为true
        self.gruc = nn.GRU(dim_rnn_input, dim_rnn_output, batch_first=True, bidirectional=True)
        self.atten_query = nn.Linear(2 * dim_rnn_output, dim_att)
        self.atten_u = nn.Linear(2 * dim_rnn_output, dim_att) # 2是因为双向网络
        self.tanh = nn.Tanh()
        self.wasser_loss = Wasserstein(t0)
        self.t0 = t0
        
        self.output_layer_t = nn.Linear(dim_rnn_output * 2, 1)
        self.output_layer_c = nn.Linear(dim_rnn_output * 2, 1)
        
        self.output_layer_final_t = nn.Linear(dim_rnn_output * 2 + dim_rnn_input, 1)
        self.output_layer_final_c = nn.Linear(dim_rnn_output * 2 + dim_rnn_input, 1)
        
    def forward(self, x, w):
        # for training
        # x: lenth, batch_size, dim_org
        # w: batch_size, 1
        # print(x.shape)
        x = self.mlp(x) # batch_size, max_time, dim_rnn_input
        # print(x.shape)
        
        xt = x[torch.where(w>0)]
        xc = x[torch.where(w<1)]
        # print(xt.shape, xc.shape)
        
        output_st, _ = self.grut(xt) # nt, t0, 2 * dim_rnn_output
        output_sc, _ = self.gruc(xc)
        
        # print(output_st.shape, output_sc.shape)
        output_yt = self.output_layer_t(output_st).squeeze(2)
        output_yc = self.output_layer_c(output_sc).squeeze(2)
        
        # print(output_yt.shape)
        
        # attention
        
        att_st = self.tanh(self.atten_query(output_st))
        att_sc = self.tanh(self.atten_query(output_sc))
        
        att_ut = self.tanh(self.atten_u(output_st))
        att_uc = self.tanh(self.atten_u(output_sc))
        # print(att_st.shape, att_ut.shape)
        
        sut = torch.sum(att_st * att_ut, dim=2, keepdim=True) # batch_size, t0, dim_att
        suc = torch.sum(att_sc * att_uc, dim=2, keepdim=True) 
        # print(sut.shape, suc.shape)
        
        alphat = nn.Softmax(dim=1)(sut)
        alphac = nn.Softmax(dim=1)(suc)
        
        output_att_st = torch.sum(alphat * output_st, dim=1)
        output_att_sc = torch.sum(alphac * output_sc, dim=1)
        # print(output_att_st.shape, output_att_sc.shape)
        x0t, x0c = xt[:, 0, :], xc[:, 0, :]
        
        y_lt_t = self.output_layer_final_t(torch.cat([output_att_st, x0t], dim=1))
        y_lt_c = self.output_layer_final_c(torch.cat([output_att_sc, x0c], dim=1))
        
        # print(y_lt_t.shape)
        
        return torch.cat([output_yt, y_lt_t], dim=1), torch.cat([output_yc, y_lt_c], dim=1), output_st, output_sc
        
    def train_model(self, train_dataset, test_dataset, epoch, lr, batch_size, lbd, decay=0.001, opt='Adam', tune_lr_every=20, gamma=0.1, verbose=10):
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        train_dl = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        pred_loss = nn.MSELoss()
        
        y_pred_train_all, y_gt_train_all, loss_all = [], [], []
        mae_train_all, mape_train_all, mae_valid_all, mape_valid_all = [], [], [], []
        y_pred_valid_all, y_gt_valid_all = [], []
        ate_pred_all, ate_gt_all = [], []
        
        if opt=='Adam':
            optimizer = optim.Adam(self.parameters(), lr=lr, weight_decay=decay)
            
        if tune_lr_every is not None and gamma is not None:
            scheduler = StepLR(optimizer, step_size=tune_lr_every, gamma=gamma)

        t0 = time.time()
        for i in range(epoch):
            
            y_pred_total, y_gt_total, local_mae_total, local_mape_total, loss_total = 0.0, 0.0, 0.0, 0.0, 0.0
            n = 0
            
            for x, w, y in train_dl:
                x, w, y = x.to(device), w.to(device), y.to(device)
                optimizer.zero_grad()
                
                y_pred_t, y_pred_c, st, sc = self.forward(x, w)
                y_gt_t = y[torch.where(w>0)]
                y_gt_c = y[torch.where(w<1)]
                
                pred_l = pred_loss(y_pred_t, y_gt_t) + pred_loss(y_pred_c, y_gt_c)
                wass_l = self.wasser_loss(st, sc)
                total_l = pred_l + lbd * wass_l
            
                total_l.backward()
                optimizer.step()
                
                # 计算评估指标
                loss_total += total_l.to('cpu').item()
                n += x.shape[0]
                with torch.no_grad():
                    y_pred_total += (y_pred_t[:, -1].sum().to('cpu').item() + y_pred_c[:, -1].sum().to('cpu').item())
                    y_gt_total += y[:, -1].sum().to('cpu').item()
                    local_mae_total += (torch.abs(y_pred_t[:, -1] - y_gt_t[:, -1]).sum().to('cpu').item() + torch.abs(y_pred_c[:, -1] - y_gt_c[:, -1]).sum().to('cpu').item())
                    local_mape_total += ((torch.abs(y_pred_t[:, -1] - y_gt_t[:, -1])/y_gt_t[:, -1]).sum().to('cpu').item() + (torch.abs(y_pred_c[:, -1] - y_gt_c[:, -1]) / y_gt_c[:, -1]).sum().to('cpu').item())
            
            y_pred_train_all.append(y_pred_total / n)
            y_gt_train_all.append(y_gt_total / n)
            mae_train_all.append(local_mae_total / n)
            mape_train_all.append(local_mape_total / n)
            loss_all.append(loss_total / n)
            
            mae_valid, mape_valid, y_pred_val, y_gt_val, ate_pred, ate_gt = self.validate(test_dataset)
            mae_valid_all.append(mae_valid)
            mape_valid_all.append(mape_valid)
            y_pred_valid_all.append(y_pred_val)
            y_gt_valid_all.append(y_gt_val)
            ate_pred_all.append(ate_pred)
            ate_gt_all.append(ate_gt)
            
            if tune_lr_every is not None and gamma is not None:
                scheduler.step()
            
            if (i + 1) % verbose == 0:
                print("[%.1f s] epoch: %d, loss: %.3f, mae train: %.3f, mape train: %.2f" % (time.time() - t0, i + 1, loss_all[-1], mae_train_all[-1], mape_train_all[-1] * 100) + "%" + 
                      ', y mae train: %.3f, y mape train: %.2f' % (y_pred_train_all[-1] - y_gt_train_all[-1], abs(y_pred_train_all[-1] - y_gt_train_all[-1]) / y_gt_train_all[-1] * 100) + '%' + 
                      ', mae train: %.3f, mape train: %.2f%%' % (mae_valid_all[-1], mape_valid_all[-1] * 100) + 
                      ', y mae valid: %.3f, y mape valid: %.2f' % (y_pred_valid_all[-1] - y_gt_valid_all[-1], abs(y_pred_valid_all[-1] - y_gt_valid_all[-1]) / y_gt_valid_all[-1] * 100) + '%' +
                      ', mae ate: %.3f, mape ate: %.2f%%' % (ate_pred_all[-1] - ate_gt_all[-1], abs((ate_pred_all[-1] - ate_gt_all[-1]) / ate_gt_all[-1]) * 100))
            
        return mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all
                
        
        
    @torch.no_grad()
    def validate(self, test_dataset):
        # 使用测试数据进行一次验证
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        test_dl = DataLoader(test_dataset, 512, shuffle=False)
        mae_valid, mape_valid = 0.0, 0.0
        y_gt_total, y_pred_total = 0.0, 0.0
        y_gt_1, y_gt_0, y_pred_1, y_pred_0 = 0.0, 0.0, 0.0, 0.0
        n, n_1, n_0 = 0, 0, 0
        for x, w, y in test_dl:
            x, w, y = x.to(device), w.to(device), y.to(device)
            y_pred_t, y_pred_c, _, _ = self.forward(x, w) # nt, t0 + 1 
            
            y_gt_t = y[torch.where(w>0)]
            y_gt_c = y[torch.where(w<1)]
            
            y_pred_total += y_pred_t[:, -1].sum().to('cpu').item()
            y_pred_total += y_pred_c[:, -1].sum().to('cpu').item()
            y_gt_total += y[:, -1].sum().to('cpu').item()
            
            mae_valid += (torch.abs(y_pred_t[:, -1] - y_gt_t[:, -1]).sum().to('cpu').item() + torch.abs(y_pred_c[:, -1] - y_gt_c[:, -1]).sum().to('cpu').item())
            mape_valid += ((torch.abs(y_pred_t[:, -1] - y_gt_t[:, -1])/y_gt_t[:, -1]).sum().to('cpu').item() + (torch.abs(y_pred_c[:, -1] - y_gt_c[:, -1]) / y_gt_c[:, -1]).sum().to('cpu').item())
            
            y_gt_1 += y_gt_t[:, -1].sum().to('cpu').item()
            y_gt_0 += y_gt_c[:, -1].sum().to('cpu').item()
            y_pred_1 += y_pred_t[:, -1].sum().to('cpu').item()
            y_pred_0 += y_pred_c[:, -1].sum().to('cpu').item()
            
            n += x.shape[0]
            n_1 += y_pred_t.shape[0]
            n_0 += y_pred_c.shape[0]
        ate_pred, ate_gt = y_pred_1 / n_1 - y_pred_0 / n_0, y_gt_1 / n_1 - y_gt_0 / n_0

        return mae_valid / n, mape_valid / n, y_pred_total / n, y_gt_total / n, ate_pred, ate_gt
            