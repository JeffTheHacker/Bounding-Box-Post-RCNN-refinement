
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
import random
from classes import *
from skimage.feature import hog
from sklearn.datasets import load_boston
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import pickle



imgArr = np.empty(0, dtype=str)
index = 0
for filename in os.listdir(r'/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_pics_down/'):
    if filename != ".DS_Store":
        imgArr = np.append(imgArr, filename)
    print(index)
    index += 1




index = 0
txtArr = np.zeros(0, dtype=str)
for filename in os.listdir(r'/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_labels_down/'):
    if filename != ".DS_Store":
        txtArr = np.append(txtArr, filename)
    print(index)
    index += 1



featurelist = np.zeros((0,11*7*2*2*9),dtype = float)
distancelist = np.empty(0, dtype = float)

count1 = 0
while (count1 < 44000):
    image_gray = cv2.imread('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_pics_down/' + imgArr[count1], cv2.IMREAD_GRAYSCALE)
    features, hog_image = hog(image_gray, orientations = 9, pixels_per_cell = (8, 8), cells_per_block = (2, 2), transform_sqrt = False, visualise = True, feature_vector = True)
    featurelist = np.append(featurelist,[features],axis = 0)
    count1 += 1
    print(count1)

count2 = 0
while count2 < 44000:
    f = open('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_labels_down/' + txtArr[count2])
    info = float(f.read())
    distancelist = np.append(distancelist,info)
    count2 += 1



pickle.dump(featurelist, open('featurelist_down.txt', 'wb'))
pickle.dump(distancelist, open('distancelist_down.txt', 'wb'))
