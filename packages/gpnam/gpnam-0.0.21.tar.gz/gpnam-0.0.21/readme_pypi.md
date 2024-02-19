# GPNAM: Gaussian Process Neural Additive Models

![The framework of GPNAM](https://github.com/Wei2624/GPNAM/blob/main/imgs/framework.jpg)
*The framework of GPNAM. `$z_s, c_s$` and the sinusoidal function are predefined from the paper and do not require training. The only trainable parameter is `W` that maps to the output of each shape function.*

This repository contains the source code for the paper Gaussian Process Neural Additive Models that appears at AAAI 2024. 

Basically, the GPNAM constructs a Neural Additive Model (NAM) by a GP with Random Fourier Features as the shape function for each input feature, which leads to a convex optimization with a significant reduction in trainable parameters. 

## Sklearn interface

You can install the package by:
```
pip install gpnam
```

Then, you can run the model simply by:
```python
from gpnam.sklearn import GPNAM

"""
input_dim: the dimensions of input data
problem: type of the task, 'classification' or 'regression'
"""
gpnam = GPNAM(input_dim, problem)
gpnam.fit(X, y)

y_pred = gpnam.predict(X_test)
```

## Citation
If you find this repo useful, please consider citing our paper:
```
@inproceedings{,
  title={Gaussian Process Neural Additive Models},
  author={Wei Zhang and Brian Barr and John Paisley},
  booktitle={AAAI Conference on Artificial Intelligence},
  year={2024}
}
```