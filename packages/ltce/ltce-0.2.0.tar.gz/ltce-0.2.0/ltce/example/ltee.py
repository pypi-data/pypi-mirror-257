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
from ..utils.dataset import LTEEDataset
from ..model.ltee import MLP, LTEE


def training_pipeline(root):
    data_path = root
    t_tar = 100
    t0 = 14

    cov_exp = pd.read_csv(data_path + 'exp data/cov_data.csv')

    y_exp = []
    for i in range(t0):
        y_exp.append(pd.read_csv(data_path + 'exp data/panel_data_%d.csv' % i)[['Y']])

    treatment_exp = pd.read_csv(data_path + 'exp data/treatment.csv')
    panel_200_exp = pd.read_csv(data_path + 'exp data/panel_data_%d.csv' % (t_tar-1)).loc[:, ['Y']]
    y_exp.append(panel_200_exp)
    y_exp = pd.concat(y_exp, axis=1)

    cov_obs = pd.read_csv(data_path + 'obs data 2/cov_data.csv')

    y_obs = []
    for i in range(t0):
        y_obs.append(pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % i).loc[:, ['Y']])

    treatment_obs = pd.read_csv(data_path + 'obs data 2/treatment.csv')
    panel_200_obs = pd.read_csv(data_path + 'obs data 2/panel_data_%d.csv' % (t_tar-1)).loc[:, ['Y']]
    y_obs.append(panel_200_obs)
    y_obs = pd.concat(y_obs, axis=1)

    n_obs, dim_input = cov_obs.shape
    n_exp, _ = cov_exp.shape
    _, dim_y = y_exp.shape


    obs_dataset = LTEEDataset(cov_obs, treatment_obs, y_obs, t0)
    exp_dataset = LTEEDataset(cov_exp, treatment_exp, y_exp, t0)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # print(device)

    dim_input = 10
    dim_rnn_input = 128
    dim_rnn_output = 256 
    dim_att=64
    t0 = 14

    lr=1e-4
    epoch=60
    tune_lr_every = 15 
    gamma = 0.1
    batch_size=256

    lbd = 1e-2 
    repeat_time = 5

    model_mlp = MLP(dim_input, dim_rnn_input).to(device)
    model_ltee = LTEE(model_mlp, dim_rnn_input, dim_rnn_output, dim_att, t0).to(device)

    mae_train_all, mape_train_all, y_gt_train_all, y_pred_train_all, mae_valid_all, mape_valid_all, y_gt_valid_all, y_pred_valid_all, ate_gt_all, ate_pred_all, loss_all\
    = model_ltee.train_model(obs_dataset, exp_dataset, lbd=lbd, lr=lr, epoch=epoch, batch_size=batch_size, tune_lr_every=tune_lr_every, gamma=gamma, verbose=2)
