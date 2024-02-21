import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader 
from torch.optim.lr_scheduler import StepLR
import time
import os
from sklearn.metrics import roc_auc_score
import random
from tqdm import tqdm
import re
from ..utils.dataset import RDataset
from ..model.rtransformer import RTransformer

def train_rtransformer(model, train_dataset, valid_dataset, epoch, batch_size=512, lr=0.0001, decoder_weight=1.0, weight_decay=0.001, shifted=False, tune_lr_every=None, gamma=None, verbose=2):
    # 将模型视为自编码器
    train_dl = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_dl = DataLoader(valid_dataset, batch_size=batch_size)
    
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    # no_wd_param = [param for name, param in model.named_parameters() if 'embedding' in name]
    # wd_param = [param for name, param in model.named_parameters() if 'embedding' not in name]
    # optimizer = optim.Adam([{'params': wd_param, 'lr':lr, 'weight_decay':weight_decay}, 
    #                         {'params': no_wd_param, 'lr':lr}])
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    f_loss = nn.MSELoss()
    c_loss = nn.BCEWithLogitsLoss()

    if tune_lr_every is not None and gamma is not None:
        scheduler = StepLR(optimizer, step_size=tune_lr_every, gamma=gamma)
    
    y_gt_train_all, y_gt_valid_all, y_pred_train_all, y_pred_valid_all, loss_all = [], [], [], [], []
    mae_train_all, mape_train_all, mae_valid_all, mape_valid_all = [], [], [], []
    y_gt_valid_1_all, y_gt_valid_0_all, y_pred_valid_1_all, y_pred_valid_0_all = [], [], [], []
    ate_pred_all, ate_gt_all, t_stat_all = [], [], []
    
    t0 = time.time()
    
    for epo in range(epoch):
        y_gt_train, y_gt_valid, y_pred_train, y_pred_valid, n_train, loss = 0.0, 0.0, 0.0, 0.0, 0, 0.0
        tt_mae_train,  tt_mape_train, tt_mae_valid, tt_mape_valid = 0.0, 0.0, 0.0, 0.0
        y_pred_valid_1, y_pred_valid_0, y_gt_valid_1, y_gt_valid_0 = 0.0, 0.0, 0.0, 0.0
        n_valid, n_valid_0, n_valid_1 = 0, 0, 0
        
        model.train()
        for x, s, w, y in train_dl:
            y = y.unsqueeze(1)
            optimizer.zero_grad()
            x, s, w, y = x.to(device), s.to(device), w.to(device), y.to(device)
            x = torch.cat([x, s, w], dim=2)

            if shifted:
                s_dec = torch.ones([s.shape[0], 1, s.shape[2]]).float().to(s.device)
                s_dec = torch.cat([s_dec, s[:, :-1, :]], dim=1)
                y_out, y_lt = model(x, s_dec) # prior_mu: batch_size, t0, dim_embedding
            else:
                y_out, y_lt = model(x, s)
            
            # print(y_out.shape, s.shape, y_lt.shape, y.shape)
            # break
            
            l =  f_loss(y_lt, y) + decoder_weight * f_loss(y_out, s) 
            l.backward()
            optimizer.step()
            
            y_gt_train += y.sum().to('cpu').item()
            y_pred_train += y_lt.sum().to('cpu').item()
            tt_mae_train += torch.abs(y - y_lt).sum().to('cpu').item()
            tt_mape_train += torch.abs((y - y_lt) / y).sum().to('cpu').item()
            
            n_train += x.shape[0]
            loss += l.to('cpu').item() * x.shape[0]
            
        # validation
        model.eval()
        with torch.no_grad():
            for x, s, w, y in valid_dl:
                x, s, w, y = x.to(device), s.to(device), w.to(device), y.to(device)
                y = y.unsqueeze(1)
                x = torch.cat([x, s, w], dim=2)
                
                s_dec = torch.ones([s.shape[0], 1, s.shape[2]]).float().to(s.device)
                s_dec = torch.cat([s_dec, s[:, :-1, :]], dim=1)
                
                if shifted:
                    s_dec = torch.ones([s.shape[0], 1, s.shape[2]]).float().to(s.device)
                    s_dec = torch.cat([s_dec, s[:, :-1, :]], dim=1)
                    _, y_lt = model(x, s_dec) # prior_mu: batch_size, t0, dim_embedding
                else:
                    _, y_lt = model(x, s)
                
                y_gt_valid += y.sum().to('cpu').item()
                y_pred_valid += y_lt.sum().to('cpu').item()
                tt_mae_valid += torch.abs(y - y_lt).sum().to('cpu').item()
                tt_mape_valid += torch.abs((y - y_lt) / y).sum().to('cpu').item()
                
                y_gt_valid_1 += y[torch.where(w[:, 0, 0]==1)].sum().to('cpu').item()
                y_gt_valid_0 += y[torch.where(w[:, 0, 0]==0)].sum().to('cpu').item()    
                
                y_pred_valid_1 += y_lt[torch.where(w[:, 0, 0]==1)].sum().to('cpu').item()
                y_pred_valid_0 += y_lt[torch.where(w[:, 0, 0]==0)].sum().to('cpu').item()                
                
                n_valid += x.shape[0]
                n_valid_1 += (w[:, 0, 0]==1).sum().to('cpu').item()
                n_valid_0 += (w[:, 0, 0]==0).sum().to('cpu').item()
        
        if tune_lr_every is not None and gamma is not None:
            scheduler.step()
                
        mae_train_all.append(tt_mae_train / n_train)
        mape_train_all.append(tt_mape_train / n_train)
        mae_valid_all.append(tt_mae_valid / n_valid)
        mape_valid_all.append(tt_mape_valid / n_valid)
        
        y_gt_train_all.append(y_gt_train / n_train)
        y_gt_valid_all.append(y_gt_valid / n_valid)
        y_pred_train_all.append(y_pred_train / n_train)
        y_pred_valid_all.append(y_pred_valid / n_valid)
        loss_all.append(loss / n_train)
        
        y_gt_valid_1_all.append(y_gt_valid_1 / n_valid_1)
        y_gt_valid_0_all.append(y_gt_valid_0 / n_valid_0)
        y_pred_valid_1_all.append(y_pred_valid_1 / n_valid_1)
        y_pred_valid_0_all.append(y_pred_valid_0 / n_valid_0)
        
        ate_gt_all.append(y_gt_valid_1 / n_valid_1 - y_gt_valid_0 / n_valid_0)
        ate_pred_all.append(y_pred_valid_1 / n_valid_1 - y_pred_valid_0 / n_valid_0)
        
        if (epo + 1) % verbose == 0:
            print("[%.1f sec], epoch: %d, loss: %.4f, mae train: %.3f, mape train: %.1f%%, y mae train: %.3f, y mape train: %.2f%%, mae valid: %.3f, mape valid: %.1f%%, y mae valid: %.3f, y mape valid: %.2f%%, mae ate: %.4f, mape ate: %.3f%%" % 
                  (time.time() - t0, epo + 1, loss_all[-1], mae_train_all[-1], mape_train_all[-1] * 100, 
                   (y_pred_train - y_gt_train) / n_train, abs(y_gt_train - y_pred_train)/ y_gt_train * 100,
                   mae_valid_all[-1], mape_valid_all[-1] * 100, 
                   (y_pred_valid - y_gt_valid) / n_valid, abs(y_gt_valid - y_pred_valid) / y_gt_valid * 100,
                   ate_pred_all[-1] - ate_gt_all[-1], abs((ate_gt_all[-1] - ate_pred_all[-1])) / ate_gt_all[-1] * 100))
            
    return mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all


def training_pipeline(root):
    # root is the directory of one of the 9 simulation datasets

    data_path = root
    t0 = 14
    t_tar = 100

    surrogate_num = 11

    print("surrogate numbers: %d" % surrogate_num)
    surro_name = ['s%d' % i for i in range(surrogate_num - 1)] + ['Y']

    cov_exp = pd.read_csv(data_path + 'exp data/cov_data.csv')
    panel_exp = []
    for i in range(t0):
        panel_exp.append(pd.read_csv(data_path + 'exp data/panel_data_%d.csv' % i)[surro_name])
    panel_exp = pd.concat(panel_exp, axis=1)
    treatment_exp = pd.read_csv(data_path + 'exp data/treatment.csv')
    panel_200_exp = pd.read_csv(data_path + 'exp data/panel_data_%d.csv' % (t_tar-1))


    cov_obs = pd.read_csv(data_path + 'obs data 2/cov_data.csv')

    panel_obs = []
    for i in range(t0):
        panel_obs.append(pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % i).loc[:, surro_name])
    panel_obs = pd.concat(panel_obs, axis=1)

    treatment_obs = pd.read_csv(data_path + 'obs data 2/treatment.csv')
    panel_200_obs = pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % (t_tar-1))

    # parameters definition
    dim_input = 11 + surrogate_num
    dim_output = surrogate_num
    dim_embedding = 64 
    n_layers = 4 
    n_heads = 8 
    dim_k = dim_v =32 
    dim_hidden = 32 
    t0 = 14
    drop=0.1
    drop_pred = 0.1
    learned_pos=True
    decoder_weight = 1.0

    verbose = 1
    weight_decay=0.001


    valid_dataset = RDataset(cov_exp, panel_exp, treatment_exp, panel_200_exp['Y'], t0)
    train_dataset = RDataset(cov_obs, panel_obs, treatment_obs, panel_200_obs['Y'], t0)
    epoch = 80
    lr=0.0002
    tune_lr_every=20 
    gamma=0.2

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = RTransformer(dim_input, dim_output, dim_embedding, n_layers, n_heads, dim_k, dim_v, dim_hidden, t0, drop=drop, drop_pred=drop_pred, learned_pos=learned_pos).to(device)
    mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all = \
    train_rtransformer(model, train_dataset, valid_dataset, epoch, weight_decay=weight_decay, lr=lr, tune_lr_every=tune_lr_every, gamma=gamma, verbose=verbose, decoder_weight=decoder_weight)

    df_res = pd.DataFrame(loss_all, columns=['loss_all'])
    df_res['mae_train_all'] = mae_train_all
    df_res['mape_train_all'] = mape_train_all
    df_res['y_gt_train_all'] = y_gt_train_all
    df_res['y_pred_train_all'] = y_pred_train_all
    df_res['mae_valid_all'] = mae_valid_all
    df_res['mape_valid_all'] = mape_valid_all
    df_res['y_gt_valid_all'] = y_gt_valid_all
    df_res['y_pred_valid_all'] = y_pred_valid_all
    df_res['ate_gt_all'] = ate_gt_all
    df_res['ate_pred_all'] = ate_pred_all
    # df_res.to_csv('./result/synthetic dataset %d/RTrans_surro_num_%d_repeat_%d.csv' % (dataset, surrogate_num, j), index=False)
    # 
