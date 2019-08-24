
# coding=utf-8
import xml.dom.minidom
import numpy as np
import os
import math
import csv
import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import re
import pandas as pd
import random
from classes import *
from sklearn.grid_search import GridSearchCV
from skimage.feature import hog
from sklearn.datasets import load_boston

from sklearn import cross_validation, metrics
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from append import distancelist1,featurelist1
import pickle


imgArr = pickle.load(open("imgarr.txt", "rb"))
txtArr = pickle.load(open("txtarr.txt", "rb"))


regressor = RandomForestRegressor(n_estimators=450,
                                  oob_score=True,
                                  verbose=2,
                                  max_features = 2000,
                                  max_depth=45,
                                  min_samples_split=2,
                                  min_samples_leaf= 1)

regressor.fit(featurelist1,distancelist1)


print(regressor.oob_score_)

pickle.dump(regressor, open('regressor_test.txt', 'wb'))


#perform gridsearch
param_test1= {'min_samples_leaf':list(range(1,10,2)),'min_samples_split':list(range(5,41,5))}
gsearch1= GridSearchCV(estimator = RandomForestRegressor(max_depth=20,
                                                         min_samples_split=9,
                                                         max_features='sqrt',
                                                         random_state=10,
                                                         n_estimators = 100,
                                                         verbose=2),
                       param_grid = param_test1, scoring=None, cv=3)
gsearch1.fit(featurelist,distancelist)
print(gsearch1.grid_scores_,gsearch1.best_params_, gsearch1.best_score_)

