from torch.utils.data import Dataset
import torch
import numpy as np
import pandas as pd

class CDataset(Dataset):
    # 输出batch, t0, dim_output, 把所有的代理指标作为trg_seq考虑
    def __init__(self, cov, proxy, treatment, result, exg, t0, length=None):
        self.x = torch.from_numpy(cov.values.astype(np.float32)).unsqueeze(1).repeat(1, t0, 1)
        self.m = torch.from_numpy(proxy.values.astype(np.float32)).view(-1, t0, proxy.shape[1] // t0)
        self.t = torch.from_numpy(treatment.values.astype(np.float32)).unsqueeze(-1).repeat(1, t0, 1)
        self.y_c = torch.from_numpy(exg.value_to_class(result.values)).long()
        self.y = torch.from_numpy(result.values.astype(np.float32))
        # self.data = torch.from_numpy(pd.concat([cov, panel], axis=1).values.astype(np.float32))
        self.length = length
    
    def __len__(self):
        return len(self.x) if self.length is None else self.length
    
    def __getitem__(self, idx):
        return self.x[idx], self.m[idx], self.t[idx], self.y_c[idx], self.y[idx]
    
    
class RDataset(Dataset):
    # 输出batch, t0, dim_output, 把所有的代理指标作为trg_seq考虑
    def __init__(self, cov, proxy, treatment, result, t0):
        self.x = torch.from_numpy(cov.values.astype(np.float32)).unsqueeze(1).repeat(1, t0, 1)
        self.m = torch.from_numpy(proxy.values.astype(np.float32)).view(-1, t0, proxy.shape[1] // t0)
        self.t = torch.from_numpy(treatment.values.astype(np.float32)).unsqueeze(-1).repeat(1, t0, 1)
        self.y = torch.from_numpy(result.values.astype(np.float32)) #.unsqueeze(1)
        # self.data = torch.from_numpy(pd.concat([cov, panel], axis=1).values.astype(np.float32))
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.m[idx], self.t[idx], self.y[idx]
    

class SIndDataset(Dataset):
    def __init__(self, cov, proxy, treatment, result):
        self.x = torch.from_numpy(cov.values.astype(np.float32))
        self.m = torch.from_numpy(proxy.values.astype(np.float32))
        self.t = torch.from_numpy(treatment.values.astype(np.float32))
        self.y = torch.from_numpy(result.values.astype(np.float32))
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.m[idx], self.t[idx], self.y[idx]
    
    
class SIndDLinearDataset(Dataset):
    def __init__(self, cov, proxy, treatment, result, t0):
        self.x = torch.from_numpy(cov.values.astype(np.float32))
        self.m = torch.from_numpy(proxy.values.astype(np.float32)).view(cov.shape[0], t0, -1)
        self.t = torch.from_numpy(treatment.values.astype(np.float32))
        self.y = torch.from_numpy(result.values.astype(np.float32))
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.m[idx], self.t[idx], self.y[idx]
    
    
class LTEEDataset(Dataset):
    def __init__(self, cov, treatment, result, t0):
        # cov shape: n, t0, 30
        # result shape: n, t0 + 1
        # treatment: n, 1
        
        x = torch.from_numpy(cov.values.astype(np.float32))
        self.x = x.unsqueeze(1).repeat(1, t0, 1)
        # print(self.x.shape)
        # self.m = torch.from_numpy(proxy.values.astype(np.float32))
        self.t = torch.from_numpy(treatment.values.astype(np.float32)).squeeze(1)
        self.y = torch.from_numpy(result.values.astype(np.float32))
        # self.data = torch.from_numpy(pd.concat([cov, panel], axis=1).values.astype(np.float32))
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.t[idx], self.y[idx]
    
    
class LASERDataset(Dataset):
    def __init__(self, cov, proxy, treatment, result):
        self.x = torch.from_numpy(cov.values.astype(np.float32))
        self.m = torch.from_numpy(proxy.values.astype(np.float32))
        self.t = torch.from_numpy(treatment.values.astype(np.float32))
        self.y = torch.from_numpy(result.values.astype(np.float32))
        # self.data = torch.from_numpy(pd.concat([cov, panel], axis=1).values.astype(np.float32))
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.m[idx], self.t[idx], self.y[idx]