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
from ..utils.dataset import SIndDataset
from ..model.sind import SIndMLP


def train_sind(model, data_train, data_valid, batch_size, epoch, lr, device, tune_lr_every, gamma, decay=0.001, verbose=10):
    loss_all, mae_train_all, mape_train_all, mae_valid_all, mape_valid_all = [], [], [], [], []
    y_gt_train_all, y_pred_train_all, y_gt_valid_all, y_pred_valid_all = [], [], [], []
    y_gt_valid_1_all, y_gt_valid_0_all, y_pred_valid_1_all, y_pred_valid_0_all = [], [], [], []
    ate_pred_all, ate_gt_all, t_stat_all = [], [], []
    
    dl_train = DataLoader(data_train, batch_size=batch_size, shuffle=True)
    dl_valid = DataLoader(data_valid, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=decay)
    scheduler = StepLR(optimizer, step_size=tune_lr_every, gamma=gamma)
    loss = nn.MSELoss()
    t0 = time.time()
    for epoch_count in range(epoch):
        
        tt_loss, local_mae_train, local_mape_train, local_mae_valid, local_mape_valid = 0.0, 0.0, 0.0, 0.0, 0.0
        y_gt_train, y_pred_train, y_gt_valid, y_pred_valid = 0.0, 0.0, 0.0, 0.0
        y_gt_valid_1, y_gt_valid_0, y_pred_valid_1, y_pred_valid_0 = 0.0, 0.0, 0.0, 0.0
        n_train, n_valid, n_valid_1, n_valid_0 = 0, 0, 0, 0
        
        for x, m, t, y in dl_train:
            optimizer.zero_grad()
            x, m, t, y = x.to(device), m.to(device), t.to(device), y.to(device)
            xm = torch.cat([x, m], dim=1)
            # print(xm.shape)
            dim_b, _ = xm.shape
            y_pred = model(xm)
            l = loss(y, y_pred)
            l.backward()
            optimizer.step()
            with torch.no_grad():
                local_mae_train += torch.abs(y - y_pred).sum().to('cpu').item()
                local_mape_train += torch.abs((y - y_pred) / y).sum().to('cpu').item()
                y_gt_train += y.sum().to('cpu').item()
                y_pred_train += y_pred.sum().to('cpu').item()
                tt_loss += l.to('cpu').item() * x.shape[0]
                n_train += x.shape[0]
                
        scheduler.step()
                
        with torch.no_grad():
            for x, m, t, y in dl_valid:
                optimizer.zero_grad()
                x, m, t, y = x.to(device), m.to(device), t.to(device), y.to(device)
                xm = torch.cat([x, m], dim=1)
                dim_b, _ = xm.shape
                y_pred = model(xm)
                
                local_mae_valid += torch.abs(y - y_pred).sum().to('cpu').item()
                local_mape_valid += torch.abs((y - y_pred) / y).sum().to('cpu').item()
                y_gt_valid += y.sum().to('cpu').item()
                y_pred_valid += y_pred.sum().to('cpu').item()            
                
                y_pred_valid_1 += y_pred[torch.where(t==1)].sum().to('cpu').item()
                y_pred_valid_0 += y_pred[torch.where(t==0)].sum().to('cpu').item()
                
                y_gt_valid_1 += y[torch.where(t==1)].sum().to('cpu').item()
                y_gt_valid_0 += y[torch.where(t==0)].sum().to('cpu').item()
                
                n_valid += dim_b
                n_valid_1 += (t==1).sum().to('cpu').item()
                n_valid_0 += (t==0).sum().to('cpu').item()
            
        loss_all.append(tt_loss / n_train)
        
        mae_train_all.append(local_mae_train / n_train)
        mape_train_all.append(local_mape_train / n_train)
        y_gt_train_all.append(y_gt_train / n_train)
        y_pred_train_all.append(y_pred_train / n_train)
        mae_valid_all.append(local_mae_valid / n_valid)
        mape_valid_all.append(local_mape_valid / n_valid)
        y_gt_valid_all.append(y_gt_valid / n_valid)
        y_pred_valid_all.append(y_pred_valid / n_valid)
        
        ate_gt_all.append(y_gt_valid_1 / n_valid_1 - y_gt_valid_0 / n_valid_0)
        ate_pred_all.append(y_pred_valid_1 / n_valid_1 - y_pred_valid_0 / n_valid_0)
        
        if (epoch_count + 1) % verbose == 0:
            print("[%.1f] epoch: %d, loss: %.3f, mae train: %.3f, mape train: %.2f%%" % (time.time() - t0, epoch_count + 1, tt_loss / n_train, mae_train_all[-1], mape_train_all[-1] * 100) + 
                  ', y mae train: %.3f, y mape train: %.2f%%' % (y_pred_train_all[-1] - y_gt_train_all[-1], abs(y_pred_train_all[-1] - y_gt_train_all[-1]) / y_gt_train_all[-1] * 100) + 
                  ', mae valid: %.3f, mape valid: %.2f%%' % (mae_valid_all[-1], mape_valid_all[-1] * 100) + 
                  ', y mae valid: %.3f, y mape valid: %.2f%%' % (y_pred_valid_all[-1] - y_gt_valid_all[-1], abs(y_pred_valid_all[-1] - y_gt_valid_all[-1]) / y_gt_valid_all[-1] * 100) + 
                  ', ate mae: %.4f, ate mape: %.2f%%' % (ate_pred_all[-1] - ate_gt_all[-1], abs((ate_gt_all[-1] - ate_pred_all[-1]) / ate_gt_all[-1]) * 100))
    return mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all


def training_pipeline(root):

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
    panel_100_exp = pd.read_csv(data_path + 'exp data/panel_data_%d.csv' % (t_tar-1))

    # n_obs = 100000
    cov_obs = pd.read_csv(data_path + 'obs data 2/cov_data.csv')

    panel_obs = []
    for i in range(t0):
        panel_obs.append(pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % i).loc[:, surro_name])
    panel_obs = pd.concat(panel_obs, axis=1)

    treatment_obs = pd.read_csv(data_path + 'obs data 2/treatment.csv')
    panel_100_obs = pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % (t_tar-1))

    n_obs, dim_x = cov_obs.shape
    n_exp, _ = cov_exp.shape
    _, dim_m = panel_exp.shape

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    data_train = SIndDataset(cov_obs, panel_obs, treatment_obs, panel_100_obs[['Y']])
    data_valid = SIndDataset(cov_exp, panel_exp, treatment_exp, panel_100_exp[['Y']])

    dim_input = 11 + surrogate_num * t0 - 1

    batch_size = 256
    epoch = 200
    tune_lr_every = 50
    gamma = 0.2
    lbd = 1
    lr = 1e-3

    model = SIndMLP(dim_input).to(device)

    mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all \
    = train_sind(model, data_train, data_valid, batch_size, epoch, tune_lr_every=tune_lr_every, gamma=gamma, lr=lr, device=device)
