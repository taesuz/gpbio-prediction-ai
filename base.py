
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings("ignore")
import sys
import os
import pandas as pd
import timeit
import numpy as np
from matplotlib import pyplot as plt
import multiprocessing as mp
import datetime as dt
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
import statsmodels.api as sm
from sklearn import linear_model as lm
import seaborn as sns
import joblib
from copy import deepcopy
from functools import partial
import math
import time
import functools
import multiprocessing as mp
from scipy.stats import norm

# from sklearn.preprocessing import OneHotEncoder
# from sklearn.ensemble import RandomForestRegressor
# import lightgbm as lgb
# from sklearn.model_selection import train_test_split

py_path = '/Users/taesuz/workspace/python/gpbio-prediction-ai/model/'

basic_path = '/Users/taesuz/workspace/python/gpbio-prediction-ai/'
data_path = PATH = basic_path + 'data/'
save_path = basic_path + 'results/'