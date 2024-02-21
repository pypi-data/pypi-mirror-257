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
from ..utils.dataset import LASERDataset
from ..utils.loss import elbo
from ..model.laser import LASER


def train_laser(model, data_obs, data_exp, batch_size, epoch, dim_z, lr, device, decay=0.001, use_prior=True, verbose=10, tune_lr_every=None, gamma=None, lbd=1.0):
    
    loss_all, mae_train_all, mape_train_all, mae_valid_all, mape_valid_all = [], [], [], [], []
    y_gt_valid_all, y_pred_valid_all, y_gt_train_all, y_pred_train_all = [], [], [], []
    y_gt_valid_1_all, y_gt_valid_0_all, y_pred_valid_1_all, y_pred_valid_0_all = [], [], [], []
    y_gt_valid_sigma_1_all, y_gt_valid_sigma_0_all, y_pred_valid_sigma_1_all, y_pred_valid_sigma_0_all = [], [], [], []
    ate_pred_all, ate_gt_all, t_stat_all = [], [], []
    
    dl_obs = DataLoader(data_obs, batch_size=batch_size, shuffle=True)
    dl_exp = DataLoader(data_exp, batch_size=batch_size, shuffle=True)
    
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=decay)
    if tune_lr_every is not None and gamma is not None:
        scheduler = StepLR(optimizer, step_size=tune_lr_every, gamma=gamma)
    
    t0 = time.time()
    for epoch_num in range(epoch):
        tt_loss, tt_mae_obs,  tt_mape_obs, tt_mae_exp, tt_mape_exp, n_train = 0.0, 0.0, 0.0, 0.0, 0.0, 0 # 需要obs和exp数据的总的loss加和，obs的mae和mape，exp的mae和mape，
        y_pred_valid_1, y_pred_valid_0, y_gt_valid_1, y_gt_valid_0 = 0.0, 0.0, 0.0, 0.0
        y_gt_train, y_pred_train, y_gt_valid, y_pred_valid = 0.0, 0.0, 0.0, 0.0
        
        model.train()
        for x, m, t, y in dl_obs:
            x, m, t, y = x.to(device), m.to(device), t.to(device), y.to(device)
            optimizer.zero_grad()
            dim_b, dim_m = m.shape
            out_encoder, out_decoder, prior_coder, out_predictor = model(x, t, m)
            loss = elbo(out_encoder, out_decoder, prior_coder, out_predictor, m, y, dim_m, dim_z, is_obs=True, use_prior=use_prior, lbd=lbd) # 损失函数是-ELBO
            
            loss.backward()
            optimizer.step()
            
            with torch.no_grad():
                tt_mae_obs += torch.abs(y - out_predictor[:, :1]).sum().to('cpu').item()
                tt_mape_obs += torch.abs((y - out_predictor[:, :1]) / y).sum().to('cpu').item()
                y_gt_train += y.sum().to('cpu').item()
                y_pred_train += out_predictor[:, :1].sum().to('cpu').item()
            tt_loss += loss.to('cpu').item()
            n_train += dim_b
            
        mae_train_all.append(tt_mae_obs / n_train)
        mape_train_all.append(tt_mape_obs / n_train)
        
        y_gt_train_all.append(y_gt_train / n_train)
        y_pred_train_all.append(y_pred_train / n_train)
        
        # 训练测试集
        for x, m, t, y in dl_exp:
            # 训练encoder、decoder和prior网络，y只用于进行validation
            x, m, t, y = x.to(device), m.to(device), t.to(device), y.to(device)
            optimizer.zero_grad()
            dim_b, dim_m = m.shape
            out_encoder, out_decoder, prior_coder, out_predictor = model(x, t, m)
            loss = elbo(out_encoder, out_decoder, prior_coder, out_predictor, m, y, dim_m, dim_z, is_obs=False, use_prior=use_prior, lbd=lbd) # 损失函数是-ELBO
            
            loss.backward()
            optimizer.step()

        
        n_valid, n_valid_1, n_valid_0 = 0, 0, 0
        
        # validation only
        model.eval()
        with torch.no_grad():
            for x, m, t, y in dl_exp:
                # 训练encoder、decoder和prior网络，y只用于进行validation
                x, m, t, y = x.to(device), m.to(device), t.to(device), y.to(device)
                dim_b, dim_m = m.shape
                out_encoder, out_decoder, prior_coder, out_predictor = model(x, t, m)
                out_predictor = out_predictor[:, 0]

                y_gt_valid += y.sum().to('cpu').item()
                y_pred_valid += out_predictor.sum().to('cpu').item()

                tt_mae_exp += torch.abs(y[:, 0] - out_predictor).sum().to('cpu').item()
                tt_mape_exp += torch.abs((y[:, 0] - out_predictor) / y[:, 0]).sum().to('cpu').item()
                
                y_pred_valid_1 += out_predictor[torch.where(t[:, 0]==1)].sum().to('cpu').item()
                y_pred_valid_0 += out_predictor[torch.where(t[:, 0]==0)].sum().to('cpu').item()
                
                y_gt_valid_1 += y[torch.where(t[:, 0]==1)].sum().to('cpu').item()
                y_gt_valid_0 += y[torch.where(t[:, 0]==0)].sum().to('cpu').item()
                
                n_valid += dim_b
                n_valid_1 += (t[:, 0]==1).sum().to('cpu').item()
                n_valid_0 += (t[:, 0]==0).sum().to('cpu').item()
                
        if tune_lr_every is not None and gamma is not None:        
            scheduler.step()
        
        loss_all.append(tt_loss / n_train)
        
        mae_valid_all.append(tt_mae_exp / n_valid)
        mape_valid_all.append(tt_mape_exp / n_valid)
        y_gt_valid_all.append(y_gt_valid / n_valid)
        y_pred_valid_all.append(y_pred_valid / n_valid)
        
        y_gt_valid_1_all.append(y_gt_valid_1 / n_valid_1)
        y_gt_valid_0_all.append(y_gt_valid_0 / n_valid_0)
        y_pred_valid_1_all.append(y_pred_valid_1 / n_valid_1)
        y_pred_valid_0_all.append(y_pred_valid_0 / n_valid_0)
        
        ate_gt_all.append(y_gt_valid_1 / n_valid_1 - y_gt_valid_0 / n_valid_0)
        ate_pred_all.append(y_pred_valid_1 / n_valid_1 - y_pred_valid_0 / n_valid_0)

        if (epoch_num + 1) % verbose == 0: 
            print("[%.2f], epoch: %d, loss: %.3f, mae train: %.3f, mape train: %.2f%%" % (time.time() -t0, epoch_num + 1, tt_loss / n_train, mae_train_all[-1], mape_train_all[-1] * 100)  + 
                  ', y mae train: %.3f, y mape train: %.2f%%' % (y_pred_train_all[-1] - y_gt_train_all[-1], abs(y_gt_train_all[-1] - y_pred_train_all[-1]) / y_gt_train_all[-1] * 100) + 
                  ', mae valid: %.3f, mape valid: %.2f' % (tt_mae_exp / n_valid, tt_mape_exp / n_valid * 100) + '%' + 
                  ', y mae valid: %.3f, y mape valid: %.2f%%' % (y_pred_valid_all[-1] - y_gt_valid_all[-1], abs(y_gt_valid_all[-1] - y_pred_valid_all[-1]) / y_gt_valid_all[-1] * 100) + 
                  ', ate mae: %.4f, ate mape: %.2f%%' % (ate_pred_all[-1] - ate_gt_all[-1], abs((ate_gt_all[-1] - ate_pred_all[-1]) / ate_gt_all[-1]) * 100) )
    return loss_all, mae_train_all, mape_train_all,y_gt_train_all, y_pred_train_all,  mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all



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

    data_train = LASERDataset(cov_obs, panel_obs, treatment_obs, panel_100_obs[['Y']])
    data_valid = LASERDataset(cov_exp, panel_exp, treatment_exp, panel_100_exp[['Y']])

    batch_size = 512
    epoch = 60 
    tune_lr_every = 15
    gamma = 0.05 
    lbd = 1
    dim_z = 8 
    lr = 1e-4 
    drop=0.0 
    complication = 1 
    verbose = 2 
    use_prior = True

    model = LASER(dim_x, dim_m, dim_z, drop, complication=complication).to(device)

    loss_all, mae_train_all, mape_train_all,y_gt_train_all, y_pred_train_all,  mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all= \
    train_laser(model, data_train, data_valid, batch_size, epoch, dim_z, lr=lr, device=device, use_prior=use_prior, tune_lr_every=tune_lr_every, gamma=gamma, lbd = lbd, verbose=verbose)
