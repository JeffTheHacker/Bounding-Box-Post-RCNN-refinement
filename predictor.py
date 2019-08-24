
# coding=utf-8
import numpy as np
import cv2
import matplotlib.image as mpimg
import csv
from skimage.feature import hog
import pickle
import os
import random

regressor_left = pickle.load(open("regressor.txt", "rb"))
regressor_right = pickle.load(open("regressor_right.txt","rb"))
regressor_up = pickle.load(open("regressor_up.txt","rb"))
regressor_down = pickle.load(open("regressor_down.txt","rb"))


def test_with_real_data(feed,repeats,xmin,ymin,xmax,ymax,count):

    image = cv2.cvtColor(feed, cv2.COLOR_BGR2GRAY)

    #left
    left_width = (ymax - ymin)* 2 / 3
    cropped_left = image[ymin:ymax, int(xmin - left_width/2):int(xmin + left_width/2),]
    resized_left = cv2.resize(cropped_left,(64,96))
    features_left, hog_image_left = hog(resized_left, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                              transform_sqrt=False, visualise=True, feature_vector=True)
    prediction_left = regressor_left.predict([features_left])[0]
    adjustment_left = prediction_left * cropped_left.shape[1]
    new_xmin = xmin + adjustment_left

    #right
    right_width = (ymax - ymin) * 2 / 3
    cropped_right = image[ymin:ymax, int(xmax - right_width/2):int(xmax + right_width/2),]
    resized_right = cv2.resize(cropped_right,(64,96))
    features_right, hog_image_right = hog(resized_right, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                              transform_sqrt=False, visualise=True, feature_vector=True)
    prediction_right = regressor_right.predict([features_right])[0]
    adjustment_right = prediction_right * cropped_right.shape[1]
    new_xmax = xmax + adjustment_right

    #up
    up_height = (xmax - xmin) * 2 / 3 * 0.75
    #cropped_up = image[int(ymin - up_height / 2):int(ymin + up_height / 2), int(xmin + (xmax - xmin) * 0.125) :int (xmax - (xmax - xmin) * 0.125),]
    cropped_up = image[int(ymin - up_height / 2):int(ymin + up_height / 2),xmin:xmax, ]
    resized_up = cv2.resize(cropped_up,(96, 64))
    features_up, hog_image_up = hog(resized_up, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                          transform_sqrt=False, visualise=True, feature_vector=True)
    prediction_up = regressor_up.predict([features_up])[0]
    adjustment_up = prediction_up * cropped_up.shape[0]
    new_ymin = ymin + adjustment_up

    #down
    down_height = (xmax - xmin) * 2 / 3 * 0.75
    cropped_down = image[int(ymax - down_height / 2):int(ymax + down_height / 2), xmin:xmax, ]
    resized_down = cv2.resize(cropped_down,(96, 64))
    features_down, hog_image_down = hog(resized_down, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                    transform_sqrt=False, visualise=True, feature_vector=True)
    prediction_down = regressor_down.predict([features_down])[0]
    adjustment_down = prediction_down * cropped_down.shape[0]
    new_ymax = ymax + adjustment_down

    new_xmin = int(new_xmin)
    new_ymin = int(new_ymin)
    new_xmax = int(new_xmax)
    new_ymax = int(new_ymax)

    if (count < repeats):
        count += 1
        new_xmin,new_ymin,new_xmax,new_ymax = test_with_real_data(feed,repeats,new_xmin,new_ymin,new_xmax,new_ymax,count)


    return new_xmin,new_ymin,new_xmax,new_ymax


def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return intersect / (sum_area - intersect)






imgArr = np.empty(0, dtype=str)
index = 0
for filename in os.listdir(r'/Users/jeffhe/Desktop/黑芝麻/boundary box regression/test_data/'):
    if filename != ".DS_Store":
        imgArr = np.append(imgArr, filename)
    index += 1


filename = '/Users/jeffhe/Desktop/黑芝麻/boundary box regression/fusion.csv'
performance = []
absolute = []
previous = []
index = 0
with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:

        if (index == 450):
            break
        xmin = int(row[0])
        ymin = int(row[1])
        xmax = int(row[2])
        ymax = int(row[3])
        length = xmax - xmin
        height = ymax - ymin
        r_xmin = xmin + random.randint(-int(length * 0.10), int(length * 0.10))
        r_xmax = xmax + random.randint(-int(length * 0.10), int(length * 0.10))
        r_ymin = ymin + random.randint(-int(height * 0.10), int(height * 0.10))
        r_ymax = ymax + random.randint(-int(height * 0.10), int(height * 0.10))
        feed = cv2.imread('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/test_data/' + imgArr[index])

        if (r_xmin < 0):
            r_xmin = 0
        if (r_xmax) >= feed.shape[1]:
            r_xmax = feed.shape[1] - 1
        if r_ymin < 0:
            r_ymin = 0
        if (r_ymax) >= feed.shape[0]:
            r_ymax = feed.shape[0] - 1

        print(r_xmin,r_xmax,r_ymin,r_ymax)
        new_xmin,new_ymin,new_xmax,new_ymax = test_with_real_data(feed, 0, r_xmin, r_ymin, r_xmax, r_ymax, 0)
        rec_truth = (ymin,xmin,ymax,xmax)
        rec_shift = (r_ymin,r_xmin,r_ymax,r_xmax)
        rec_predict = (new_ymin,new_xmin,new_ymax,new_xmax)
        IOU_before = compute_iou(rec_truth, rec_shift)
        IOU_after = compute_iou(rec_truth, rec_predict)
        improvement = (IOU_after - IOU_before) / IOU_before
        performance.append(improvement)
        absolute.append(IOU_after)
        previous.append(IOU_before)

        feed = cv2.rectangle(feed, (xmin, ymin), (xmax, ymax), (255, 0, 0), 1)
        feed = cv2.rectangle(feed, (r_xmin, r_ymin), (r_xmax, r_ymax), (0, 255, 0), 2)
        feed = cv2.rectangle(feed, (new_xmin, new_ymin), (new_xmax, new_ymax), (0, 0, 255), 3)
        cv2.imwrite('/Users/jeffhe/Desktop/results/6/' + str(index).zfill(6) + '.png',feed)

        index += 1

print('average improvement')
print(sum(performance) / len(performance))
count = 0
for i in performance:
    if i < 0:
        count += 1
print('negative improvement rate')
print(count / len(performance))
print('improved average IOU')
print(sum(absolute)/len(absolute))
print('IOU average before ')
print(sum(previous) / len(previous))










