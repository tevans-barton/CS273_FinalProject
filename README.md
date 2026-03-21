# CS273_FinalProject
Sayan Andrews

Austin Sunwoo Lee

Thomas Evans-Barton

## Project Overview
In this project we aimed to build a binary classifier to predict whether or not a college basketball team would advance past the first round of the tournament, using the team's regular season statistics as a predictor.

## Setup Instructions
If you would like to see how we constructed our dataset from the raw data in the [*March Machine Learning Mania 2026*](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) competition from Kaggle, feel free to look at our etl.py file. We have uploaded this constructed dataset in data/final.csv for your convenience.

## How to Train the Model
Open `demo.ipynb` and run all cells top to bottom. The notebook reads
`data/final.csv`, standardizes the 15 per-game features, and runs
stratified 5-fold cross-validation training the MLP for 300 epochs per fold.

## How to Evaluate the Model
Evaluation runs automatically within the notebook. After the
cross-validation loop completes, the final cell prints a side-by-side
comparison of the MLP against the random baseline showing accuracy
and AUC-ROC for each fold and the mean ± std across all 5 folds.

## Expected Outputs
- Per-fold accuracy and AUC-ROC printed to the console after each fold
- Aggregate mean ± std summary across all 5 folds
- `training_curve.png` saved to the working directory — train vs.
  validation BCE loss plotted over 300 epochs for fold 1
- Final summary table comparing MLP [128, 64, 32] against the
  random baseline (0.500 acc / 0.500 AUC)

## Required Dependencies
Install all dependencies before running the notebook:
```bash
pip install torch numpy pandas scikit-learn matplotlib
```

The following imports are used across `etl.py` and `demo.ipynb`:
```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
```

