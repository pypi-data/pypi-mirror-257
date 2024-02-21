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
This project is established based on pytorch. Before installing the ltce packages, please go to https://pytorch.org/ to download a suitable pytorch version.
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


-----------------------
Examples for Using ltce 
-----------------------
This section would demonstrate an example for each model.

++++++++++++++++++
Preparing datasets
++++++++++++++++++

A simulation dataset could be downloaded via::

    git clone https://github.com/zhangyuanyuzyy/LT-Transformer-Dataset.git 


Unpack the downloaded dataset and put directory `dataset` under a given `root` directory, such that
::

    .root
    └── dataset
        ├── synthetic dataset 1
        ├── synthetic dataset 2
        ├── synthetic dataset 3
        ├── synthetic dataset 4
        ├── synthetic dataset 5
        ├── synthetic dataset 6
        ├── synthetic dataset 7
        ├── synthetic dataset 8
        └── synthetic dataset 9

At present, synthetic dataset 7, 8 and 9 are not available because they are relatively large. The basic information of these 9 datasets are shown in the table below.

+---------+--------------------+-------+---------------+
| Dataset |   Size(Obs, Exp)   |  SNR  | Estimated SNR |
+=========+====================+=======+===============+
|1        |5000,2000           |2.11   |17.73          |
+---------+--------------------+-------+---------------+
|2        |5000,2000           |7.32   |41.13          |
+---------+--------------------+-------+---------------+
|3        |5000,2000           |93.08  |50.64          |
+---------+--------------------+-------+---------------+
|4        |50000,20000         |2.33   |3.73           |
+---------+--------------------+-------+---------------+
|5        |50000,20000         |9.10   |44.17          |
+---------+--------------------+-------+---------------+
|6        |50000,20000         |77.33  |362.79         |
+---------+--------------------+-------+---------------+
|7        |1000000,500000      |2.13   |1.46           |
+---------+--------------------+-------+---------------+
|8        |1000000,500000      |10.16  |32.26          |
+---------+--------------------+-------+---------------+
|9        |1000000,500000      |94.24  |56.80          |
+---------+--------------------+-------+---------------+

+++++++++++++
Running model
+++++++++++++
If dataset and ltce are both ready, you could run our examples via ::

    from ltce.example.{testmodel} import training_pipeline

    dataset = '{root}' + '/dataset/synthetic dataset {testdataset}/'
    training_pipeline(dataset)

`root` is the root directory where you put the downloaded dataset.
`testmodel` could be chosen from rtransformer, ctransformer, sind_linear, sind_mlp, sind_dlinear, ltee, laser
`testdataset` could be chosen between 1 and 9. However, the hyper-parameters setting are only suitable for dataset 1, 2 and 3, which is recommended as a starting point.
Below shows 3 concrete examples of running ltce models. Suppose the root directory is `home/`. Replace it with your own directory.

1. R Transformer::

    from ltce.example.rtransformer import training_pipeline

    dataset = 'home/dataset/synthetic dataset 3/'
    training_pipeline(dataset)


2. SInd-DLinear::

    from ltce.example.sind_dlienar import training_pipeline

    dataset = 'home/dataset/synthetic dataset 3/'
    training_pipeline(dataset)


3. LTEE::

    from ltce.example.ltee import training_pipeline

    dataset = 'home/dataset/synthetic dataset 3/'
    training_pipeline(dataset)


-------------
About Version 
-------------
+++++++++++++
version 0.2.0
+++++++++++++
Running examples for each model were supplemented. These examples are suitable for users to learn how to work with ltce.

+++++++++++++
version 0.1.0
+++++++++++++
This is the first stable version of ltce. It contained models 7 models, including 3 SInd-based model (SInd-Linear, SInd-MLP, SInd-DLinear), 2 transformer-based models (R Transformer, C Transformer), LTEE and LASER.

+++++++++++++++
version 0.1.0b1
+++++++++++++++
This is the first beta version of ltce. Happily, it was born with two transformer-based models, CTransformer and RTransformer. More models would be included in the future versions.


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