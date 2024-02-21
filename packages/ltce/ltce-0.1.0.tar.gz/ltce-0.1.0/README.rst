====================================================
Long-Term Causal Effect (ltce), Brief Description 
====================================================
Estimating the long-term treatment impact is crucial in many areas such as business and medicine.  The main difficulty of this problem is that observing the long-term effect requires unacceptable costs and duration typically far longer than the decision-making window. The Long-term causal effect packages provided an integration of recent progress in this problem, including models such as SInd, LT-Transformer. This sort of method would typically utilize two datasets, one contains observed long-term outcomes for model training and another one with unobserved long-term outcomes to be predicted.

------------------
Install Guidelines
------------------
Below shows how to install and use ltce packages.

+++++++++++++++++++++
Requirements for ltce
+++++++++++++++++++++
This project is established based on pytorch. Before install the ltce packages, please go to https://pytorch.org/ to download a suitable pytorch version.
The pytorch with cuda is preferred due to efficiency reason.
Once pytorch is ready, you can move to the next step.

++++++++++++++++++++++++
Download model & dataset
++++++++++++++++++++++++
ltce could be installed via::

    pip install ltce 

or ::

    pip install ltce --index-url https://pypi.org/simple 

in case the mirror does not synchronized the newest version.


++++++++++++
Using models
++++++++++++

The long-term effect estimation problem typically requires 2 dataset, one observational dataset with the desired long-term outcomes, and an experimental dataset where long-term outcome is missing.
Each dataset contains 4 types of data: the covariate (X), the treatment (W), the surrogates (S) and the long-term outcome (Y).
The requirement for each model is as below

+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|    model        | X(obs) | W(obs) | S(obs) | Y(obs) | X(exp) | W(exp) | S(exp) | Y(exp) |
+=================+========+========+========+========+========+========+========+========+
|SInd-Linear [1]  |   Y    |   N    |   Y    |   Y    |   Y    |   N    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|SInd_MLP [2]     |   Y    |   N    |   Y    |   Y    |   Y    |   N    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|SInd-DLinear [4] |   Y    |   N    |   Y    |   Y    |   Y    |   N    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|LTEE [3]         |   Y    |   Y    |   N    |   Y    |   Y    |   Y    |   N    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|LASER [2]        |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|R Transformer    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+
|C Transformer    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   Y    |   N    |
+-----------------+--------+--------+--------+--------+--------+--------+--------+--------+  


-------------
About Version 
-------------
+++++++++++++
version 0.1.0
+++++++++++++
This is the first stable version of ltce. It contained models 7 models, including 3 SInd-based model (SInd-Linear, SInd-MLP, SInd-DLinear), 2 transformer-based models (R Transformer, C Transformer), LTEE and LASER.

+++++++++++++++
version 0.1.0b1
+++++++++++++++
This is the first beta version of ltce. Happily, it was born with two transformer-based models, CTransformer and RTransformer. More models would be included in the future versions.


----------
An Example 
----------
A simulation dataset could be downloaded via::

    git clone https://github.com/zhangyuanyuzyy/LT-Transformer-Dataset.git 


Unpack the downloaded dataset and put directory `dataset` under the `LT-Transformer` directory, such that
::

    .(LT-Transformer)
    ├── dataset
    │   ├── synthetic dataset 1
    │   ├── synthetic dataset 2
    │   ├── synthetic dataset 3
    │   ├── synthetic dataset 4
    │   ├── synthetic dataset 5
    │   ├── synthetic dataset 6
    │   ├── synthetic dataset 7
    │   ├── synthetic dataset 8
    │   └── synthetic dataset 9
    ├── experiment
    └── model 

++++++++++
Parameters
++++++++++


+++++++++++++
Running model
+++++++++++++
1. Simulation data for R Transformer
::

    python simulation.py -m r_transformer -r 5 -d 3 -s 11 


2. Simulation data for C Transformer
::

    python simulation.py -m c_transformer -r 5 -d 3 -s 11 



----------
References
----------
[1] Susan Athey, Raj Chetty, Guido Imbens, and Hyunseung Kang. 2019. The Surrogate Index: Combining Short-Term Proxies to Estimate Long-Term TreatmentEffects More Rapidly and Precisely. Randomized Social Experiments eJournal (2019).
[2] Ruichu Cai, Weilin Chen, Zeqin Yang, Shu Wan, Chen Zheng, Xiaoqing Yang, and Jiecheng Guo. 2022. Long-term Causal Effects Estimation via Latent Surrogates Representation Learning. ArXiv abs/2208.04589 (2022).
[3] Lu Cheng, Ruocheng Guo, and Huan Liu. 2020. Long-Term Effect Estimation with Surrogate Representation. Proceedings of the 14th ACM International Conference on Web Search and Data Mining (2020).
[4] Ailing Zeng, Mu-Hwa Chen, L. Zhang, and Qiang Xu. 2022. Are Transformers Effective for Time Series Forecasting?. In AAAI Conference on Artificial Intelligence.

Part of the code in this package is based on the followings references:
1. https://github.com/siamakz/iVAE/
2. https://github.com/zhangyuanyuzyy/LT-Transformer