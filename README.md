# Stereo Calibration
The difference between single camera calibration and binocular camera system is that the binocular camera system should calibrate the transform between the left and the right camera. According to the blog:https://blog.csdn.net/xuelabizp/article/details/50417914, we can get the transform using these equations:
R=R_rR^T_l, \\
T=T_r-RT_L, 
Since we can get the rotation matrix and transform matrix with the help of OpenCV functions. We can simply get the transform between two cameras by the operation of matrix. The source code: https://github.com/Dhtu/StereoCali.git
## load image
First, we load the image data in fold "data\left","data\right"
```python
if datatype == '1':
            tempimg = cv.imread(path)
            loadimg(tempimg)
			
```
## single camera calibration
Then, calibrate two cameras and we can get the Intrinsic parameters and External parameters.
```python
retvalL, camtxL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpoints, tempimg.shape[:2], None, None)
retvalR, camtxR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpoints, tempimg.shape[:2], None, None)
```
I save it in the .npy file for further use.
## matrix operation
Finally, calculate the transform according to the equations mentioned above
```python
for n in range(12):
    rmtxL = cv.Rodrigues(rvecsL[n])
    rmtxR = cv.Rodrigues(rvecsR[n])
    rmtx = np.dot(rmtxR[0], rmtxL[0].T)
    tvec=tvecsR[n]-np.dot(rmtx,tvecsL[n])
	
	```