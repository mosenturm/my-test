# -*- coding: utf-8 -*-
# taken from
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html
#
import os
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt


base_dir = os.getcwd() + "/assets"
print base_dir
catalog_dir = "/sets"

#print base_dir + '/llanowar_snap.jpg'
snapImg = base_dir + '/llanowar_snap.jpg'
img = cv2.imread(snapImg) # trainImage from camera scan
#print "snapImg.shape before: " + str(img.shape)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print "snapImg.shape after: " + str(img.shape)
#print img
ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#ret,contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]


# Let cnt be the contour and img be the input

rect = cv2.minAreaRect(cnt)
#box = cv2.boxPoints(rect)
box = cv2.cv.boxPoints(rect)
box = np.int0(box)
print "Angle: " + rect[2]

W = rect[1][0]
H = rect[1][1]

Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)

angle = rect[2]
if angle < -45:
    angle += 90

# Center of rectangle in source image
center = ((x1+x2)/2,(y1+y2)/2)
# Size of the upright rectangle bounding the rotated rectangle
size = (x2-x1, y2-y1)
M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)
# Cropped upright rectangle
cropped = cv2.getRectSubPix(img, size, center)
cropped = cv2.warpAffine(cropped, M, size)
croppedW = H if H > W else W
croppedH = H if H < W else W
# Final cropped & rotated rectangle
croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW),int(croppedH)), (size[0]/2, size[1]/2))

cv2.imwrite(base_dir + '/llanowar_rotate-crop.jpg', croppedRotated)