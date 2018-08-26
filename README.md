# Stereo Calibration
The difference between single camera calibration and binocular camera system is that the binocular camera system should calibrate the transform between the left and the right camera. According to the blog:https://blog.csdn.net/xuelabizp/article/details/50417914, we can get the transform using these equations:
			\begin{equation}
			\left\{
							\begin{array}{lr}
							R=R_rR^T_l, & \\
							T=T_r-RT_L, &
							\end{array}
			\right.
			\end{equation}
		Since we can get the rotation matrix and transform matrix with the help of OpenCV functions. We can simply get the transform between two cameras by the operation of matrix. The source code: https://github.com/Dhtu/StereoCali.git
		