
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


# obtain list of xml names
xmlArr = np.empty(0, dtype=str)
for filename in os.listdir(r'/Users/jeffhe/Desktop/黑芝麻/boundary box regression/Annotations'):
    if filename != ".DS_S.xml":
        xmlArr = np.append(xmlArr, filename)

# obtain list of images
imgArr = np.empty(0, dtype=str)
for i in xmlArr:
    imgArr = np.append(imgArr,i[0:6] + '.png')

print(len(imgArr),len(xmlArr))


lenConst = len(xmlArr)
count = 0
boundboxes = []

# put everything into a list of objects
while count < lenConst:
    print(count)
    # get names
    xmlName = xmlArr[count]
    imgName = imgArr[count]
    # get image file
    image = mpimg.imread('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_images/' + imgName)
    # generate object
    boundbox = img_with_box(image,imgName[0:6])
    boundboxes.append(boundbox)
    # get xml files
    dom = xml.dom.minidom.parse('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/Annotations/' + xmlName)
    root = dom.documentElement
    objList = root.getElementsByTagName('object')
    # for each file, append the boxes to the object
    for i in objList:
        name = i.getElementsByTagName('name')[0].firstChild.data
        bbox = i.getElementsByTagName('bndbox')[0]
        occluded = int(bbox.getElementsByTagName('occluded')[0].firstChild.data)
        xmin = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)
        ymin = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)
        xmax = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)
        ymax = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)
        boundbox.appendBbox(name, occluded, xmin, ymin, xmax, ymax)
    # increment count
    count += 1

#now we have a list of boundboxes, with each element corresponding to each image file in order
#every bound box object contains the image as well as the multiple bboxes that it contains

#filter the bounding boxes: remove anything that's not from a car or too small
for i in boundboxes: #with respect to each image
    removeList = []
    for j in i.getbboxList(): #with respect to the bounding boxes in the image
        if j.getName() != 'Car':
            removeList.append(j)
        elif j.getArea() < 750:
            removeList.append(j)
        elif j.getOccluded() != 0:
            removeList.append(j)
    for k in removeList:
        i.removebboxfromlist(k)

#array that contains img_with_side_enum objects
enumerated_boxes = []

#now, we have filtered image objects that each contain suitable bounding boxes
#next step: convert every img_with_box object into img_with_side_enum object
for i in boundboxes:
    #first create the new enumerated box object and add it to the list
    enumerated_box = img_with_side_enum(i.getImage(),i.getID())
    enumerated_boxes.append(enumerated_box)
    for j in i.getbboxList(): #j is a bbox object containing coordinates and name and occlusion state
        #make modifications directly on the enumerated_box
        enumerated_box.generation(j.getCoordinates()[0],j.getCoordinates()[1],j.getCoordinates()[2],j.getCoordinates()[3])


#check the validity for each enumerated box
for i in enumerated_boxes: #i represents image_with_side_enum object
    #clean up left borders
    removeList = []
    for j in i.getLeftBorderList(): #j represents enumeration object
        #print('reached')
        result = j.selfCheck()
        if result == False:
            removeList.append(j)
    for k in removeList:
        i.getLeftBorderList().remove(k)


    #clean up right borders
    removeList = []
    for j in i.getRightBorderList(): #j represents enumeration object
        if j.selfCheck() == False:
            removeList.append(j)
    for k in removeList:
        i.getRightBorderList().remove(k)


    #clean up up borders
    removeList = []
    for j in i.getUpBorderList(): #j represents enumeration object
        if j.selfCheck() == False:
            removeList.append(j)
    for k in removeList:
        i.getUpBorderList().remove(k)


    #clean down right borders
    removeList = []
    for j in i.getDownBorderList(): #j represents enumeration object
        if j.selfCheck() == False:
            removeList.append(j)
    for k in removeList:
        i.getDownBorderList().remove(k)



#now crop out the images regarding the coordinates of the enumerated box, resize them and then save.
index = 0
for i in enumerated_boxes:
    image = i.getImage()
    #for left border
    for j in i.getLeftBorderList():
        distance = j.getDistance()
        cropped = image[j.getCoordinates()[1]:j.getCoordinates()[3],j.getCoordinates()[0]:j.getCoordinates()[2],]
        width, height = cropped.shape[1], cropped.shape[0]
        cropped = cv2.resize(cropped, (64, 96))
        distance = distance/width
        print(distance)
        cv2.imwrite('/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_pics/' + str(index).zfill(6) + ".png", cv2.cvtColor(cropped*255, cv2.COLOR_RGB2BGR))
        text_create(str(index).zfill(6) + '.txt',str(distance))
        index += 1










