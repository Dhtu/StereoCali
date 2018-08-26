#!/usr/bin/env python
# Path_generation
# use UTF-8
# Python 3.6.3

import cv2 as cv
import numpy as np
import os

# criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

label_map = {
    'left': 0,
    'right': 1
}

with open('data.txt', 'w') as f:
    for root, dirs, files in os.walk('data'):
        for filename in files:
            filepath = os.sep.join([root, filename])
            dirname = root.split(os.sep)[-1]
            label = label_map[dirname]
            line = '{},{}\n'.format(filepath, label)
            f.write(line)

inner_conner_num = (9, 6)
inner_conner_width = 9
inner_conner_hight = 6
# initial the vector of objectpoints
obpoint = np.zeros((9 * 6, 3), np.float32)
obpoint[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
# obpoint *= 30
objpoints = []
imgpoints = []
tempimg = cv.imread('data\left\left01.jpg')


# print(obpoint)


def loadimg(img):
    # grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    retval, corners = cv.findChessboardCorners(img, inner_conner_num)
    # corners2 = cv.cornerSubPix(img, corners, (10, 10), (-1, -1), criteria)
    objpoints.append(obpoint)
    imgpoints.append(corners)


# load images which is listed in data.txt
with open('data.txt', 'r') as data:
    lines = data.readlines()
    for line in lines:
        path, datatype = line.rstrip().split(',')
        # only process the left data
        if datatype == '0':
            tempimg = cv.imread(path)
            loadimg(tempimg)
    # camera calibration
    retvalL, camtxL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpoints, tempimg.shape[:2], None, None)
    np.save("camera_matrixL", camtxL)  # Internal parameter matrix
    np.save("distortion_cofficientsL", distL)  # distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    np.save("rotation_vectorsL", rvecsL)  # rotation vectors
    np.save("translation_vectorsL", tvecsL)  # translation vectors

with open('data.txt', 'r') as data:
    lines = data.readlines()
    for line in lines:
        path, datatype = line.rstrip().split(',')
        # only process the left data
        if datatype == '1':
            tempimg = cv.imread(path)
            loadimg(tempimg)
    # camera calibration
    retvalR, camtxR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpoints, tempimg.shape[:2], None, None)
    np.save("camera_matrixR", camtxR)  # Internal parameter matrix
    np.save("distortion_cofficientsR", distR)  # distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    np.save("rotation_vectorsR", rvecsR)  # rotation vectors
    np.save("translation_vectorsR", tvecsR)  # translation vectors
rmtxset = []
tvecset=[]
for n in range(12):
    rmtxL = cv.Rodrigues(rvecsL[n])
    rmtxR = cv.Rodrigues(rvecsR[n])
    rmtx = np.dot(rmtxR[0], rmtxL[0].T)
    tvec=tvecsR[n]-np.dot(rmtx,tvecsL[n])
    # print(tvec)
    rmtxset.append(rmtx)
    tvecset.append(tvec)
    np.save("rotation_mat",rmtxset)
    np.save("teanslation_vectors",tvecset)
# undistort
# for line in lines:
#     path, datatype = line.rstrip().split(',')
#     if datatype == '0':
#         tempimg = cv.imread(path)
#         new_camtx, roi = cv.getOptimalNewCameraMatrix(camtx, dist, tempimg.shape[:2], 0)
#         dstimg = cv.undistort(tempimg, camtx, dist, None, new_camtx)
#         # save at a new folder
#         path1, path2, path3 = path.split('\\')
#         new_path = '{}\\new{}\{}'.format(path1, path2, path3)
#         cv.imwrite(new_path, dstimg)


# calculate the error of the process above:0.04965026811058618
# total_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], camtx, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
#     total_error += error
# print("total error: ", total_error / len(objpoints))
