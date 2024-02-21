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
from ..utils.dataset import CDataset
from ..utils.splitter import UniformSplitter
from ..model.ctransformer import CTransformer

def train_ctransformer(model, train_dataset, valid_dataset, exg, epoch, use_treatment=True, batch_size=256, lr=0.0001, weight_decoder=1.0, weight_decay=0.001, tune_lr_every=None, gamma=None, verbose=2,
                       device='cuda' if torch.cuda.is_available() else 'cpu'):
    train_dl = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_dl = DataLoader(valid_dataset, batch_size=batch_size)
    
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    # no_wd_param = [param for name, param in model.named_parameters() if 'embedding' in name]
    # wd_param = [param for name, param in model.named_parameters() if 'embedding' not in name]
    # optimizer = optim.Adam([{'params': wd_param, 'lr':lr, 'weight_decay':weight_decay}, 
    #                         {'params': no_wd_param, 'lr':lr}])
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    f_loss = nn.MSELoss()
    c_loss = nn.CrossEntropyLoss()#None if exg.weight is None else torch.Tensor(exg.weight).to(device))
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
        for x, s, w, y_c, y in train_dl:
            optimizer.zero_grad()
            x, s, w, y_c, y = x.to(device), s.to(device), w.to(device), y_c.to(device), y.to(device)
            if use_treatment:
                x = torch.cat([x, s, w], dim=2)
            else:
                x = torch.cat([x, s], dim=2)
            y_out, y_lt = model(x, s) # prior_mu: batch_size, t0, dim_embedding
            l = weight_decoder * f_loss(y_out, s) + c_loss(y_lt, y_c)
            l.backward()
            optimizer.step()
            
            y_pred = torch.from_numpy(exg.class_to_value(torch.argmax(y_lt, dim=1).to('cpu').detach().numpy())).to(y.device)
            
            y_gt_train += y.sum().to('cpu').item()
            y_pred_train += y_pred.sum()
            
            tt_mae_train += torch.abs(y - y_pred).sum().to('cpu').item()
            tt_mape_train += torch.abs((y - y_pred) / y).sum().to('cpu').item()
            
            n_train += x.shape[0]
            loss += l.to('cpu').item() * x.shape[0]
            
        # validation
        model.eval()
        with torch.no_grad():
            for x, s, w, y_c, y in valid_dl:
                x, s, w, y_c, y = x.to(device), s.to(device), w.to(device), y_c.to(device), y.to(device)
                # print(x.shape, s.shape, w.shape, y_c.shape, y.shape)
                if use_treatment:
                    x = torch.cat([x, s, w], dim=2)
                else:
                    x = torch.cat([x, s], dim=2)
                _, y_lt = model(x, s)
                y_pred = torch.from_numpy(exg.class_to_value(torch.argmax(y_lt, dim=1).to('cpu').detach().numpy())).to(y.device)
                
                y_gt_valid += y.sum().to('cpu').item()
                y_pred_valid += y_pred.sum()
                
                tt_mae_valid += torch.abs(y - y_pred).sum().to('cpu').item()
                tt_mape_valid += torch.abs((y - y_pred) / y).sum().to('cpu').item()
                
                y_gt_valid_1 += y[torch.where(w[:, 0, 0]==1)].sum().to('cpu').item()
                y_gt_valid_0 += y[torch.where(w[:, 0, 0]==0)].sum().to('cpu').item()    
                
                y_pred_valid_1 += y_pred[torch.where(w[:, 0, 0]==1)].sum().to('cpu').item()
                y_pred_valid_0 += y_pred[torch.where(w[:, 0, 0]==0)].sum().to('cpu').item()                
                
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
            print("[%.1f sec], epoch: %d, loss: %.3f, mae train: %.3f, mape train: %.1f%%, y mae train: %.3f, y mape train: %.2f%%, mae valid: %.3f, mape valid: %.1f%%, y mae valid: %.3f, y mape valid: %.2f%%, mae ate: %.4f, mape ate: %.3f%%" % 
                  (time.time() - t0, epo + 1, loss_all[-1], mae_train_all[-1], mape_train_all[-1] * 100, 
                   (y_pred_train - y_gt_train) / n_train, abs(y_gt_train - y_pred_train)/ y_gt_train * 100,
                   mae_valid_all[-1], mape_valid_all[-1] * 100, 
                   (y_pred_valid - y_gt_valid) / n_valid, abs(y_gt_valid - y_pred_valid) / y_gt_valid * 100,
                   ate_pred_all[-1] - ate_gt_all[-1], abs((ate_gt_all[-1] - ate_pred_all[-1]) / ate_gt_all[-1] * 100)))
            
    return mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all


def training_pipeline(root):

    data_path = root
    t0 = 14
    t_tar = 100
    dim_class = 256
    use_treatment = True

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


    exg = UniformSplitter(panel_200_obs[['Y']], dim_class)

    dim_input = (11 + surrogate_num) if use_treatment else (10 + surrogate_num)
    dim_output = surrogate_num
    dim_embedding =  64
    n_layers = 6
    n_heads = 8 
    dim_k = dim_v = 32
    dim_hidden =  64
    t0 = 14
    drop=0.1
    drop_pred = 0.1 
    learned_pos=True

    verbose = 1
    weight_decay=0.001 

    valid_dataset = CDataset(cov_exp, panel_exp, treatment_exp, panel_200_exp['Y'], exg, t0)
    train_dataset = CDataset(cov_obs, panel_obs, treatment_obs, panel_200_obs['Y'], exg, t0)
    epoch = 60
    lr= 0.001 # 5e-4
    tune_lr_every = 20 
    gamma=0.1

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = CTransformer(dim_input, dim_output, dim_embedding, n_layers, n_heads, dim_k, dim_v, dim_hidden, dim_class, t0, drop=drop, drop_pred=drop_pred, learned_pos=learned_pos).to(device)
    mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all = \
    train_ctransformer(model, train_dataset, valid_dataset, exg, epoch, weight_decay=weight_decay, lr=lr, tune_lr_every=tune_lr_every, gamma=gamma, verbose=verbose, use_treatment=use_treatment)