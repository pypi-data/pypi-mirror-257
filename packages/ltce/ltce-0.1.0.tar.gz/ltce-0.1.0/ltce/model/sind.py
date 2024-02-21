import torch
import torch.nn as nn


class SInd(nn.Module):
    # Linear model
    def __init__(self, input_dim):
        super(SInd, self).__init__()
        self.ind = nn.Linear(input_dim, 1)
        
    def forward(self, X):
        return self.ind(X)
    
    
class SInd_MLP(nn.Module):

    def __init__(self, input_dim):
        super(SInd_MLP, self).__init__()
        self.layer1 = nn.Linear(input_dim, 256)
        self.layer2 = nn.Linear(256, 512)
        self.layer3 = nn.Linear(512, 1)
        self.lrelu = nn.LeakyReLU()
        self.tanh = nn.Tanh()
        self.drop = nn.Dropout(0.5)
        
    def forward(self, X):
        X = self.tanh(self.layer1(X))
        X = self.tanh(self.layer2(X))
        return self.lrelu(self.layer3(X))
        
        
class MovingAvg(nn.Module):
    # code references: 
    def __init__(self, kernel_size, stride):
        super(MovingAvg, self).__init__()
        self.kernel_size = kernel_size
        self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=stride, padding=0)

    def forward(self, x):
        # padding on the both ends of time series
        front = x[:, 0:1, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        end = x[:, -1:, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        x = torch.cat([front, x, end], dim=1)
        x = self.avg(x.permute(0, 2, 1))
        x = x.permute(0, 2, 1)
        return x


class SeriesDecomp(nn.Module):
    def __init__(self, kernel_size):
        super(SeriesDecomp, self).__init__()
        self.moving_avg = MovingAvg(kernel_size, stride=1)

    def forward(self, x):
        moving_mean = self.moving_avg(x)
        res = x - moving_mean
        return res, moving_mean
        
        
class SInd_Decom(nn.Module):
    def __init__(self, input_dim_cov, input_dim_series, kernel_size=7):
        super(SInd_Decom,self).__init__()

        # Decompsition Kernel Size
        # kernel_size = 7
        self.decompsition = SeriesDecomp(kernel_size)

        self.linear_seasonal = nn.Linear(input_dim_series,1)
        self.linear_trend = nn.Linear(input_dim_series,1)
        self.linear_cov = nn.Linear(input_dim_cov, 1)
    
    def forward(self, x_cov, x_series):
        # x_series: [Batch, Input length, Channel]
        # x_cov: Batch, Input length
        seasonal_init, trend_init = self.decompsition(x_series)
        seasonal_init, trend_init = seasonal_init.view(x_cov.shape[0], -1), trend_init.view(x_cov.shape[0], -1)

        seasonal_output = self.linear_seasonal(seasonal_init)
        trend_output = self.linear_trend(trend_init)
        cov_output = self.linear_cov(x_cov)

        x = seasonal_output + trend_output + cov_output
        return x # to [Batch, 1]