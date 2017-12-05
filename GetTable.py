#!/usr/bin/env python
# -*- Python -*-
import sys
import os
import time
import copy
import threading
import math
from Algorithm import*
import numpy as np

pi = np.pi

#import world path ===================
import WorkspaceDirInfo as shareDir
sys.path.append(shareDir.WorkspaceDir)
import share.tools.geo.geo as geo
from share.tools.classes.f21pa10Class import fpa10Class
from share.data.handCamCalib.Th2c_ir import*
from share.tools.classes.parallelGripperClass import parallelGripperClass

#import local path ===================
sys.path.append(os.path.join(".."))
import set_env
baseDir = shareDir.WorkspaceDir + set_env.MyName
sys.path.append(baseDir)
from tools.classes.realsenseClass import realsenseClass

################initial###########################################
print "initial pa10"
arm = fpa10Class("_l") 

print "initial RealSense"
realsense = realsenseClass()
print "initial Over"

base_xyzabc =[0.65, 0, 0.20, 0, 0, 0]
#base_xyzabc =[0.50, 0.0, 0.55, 0, 0, 0]
# change mode joint  and  move ready pose
print "mode joint"
arm.mode_joint()
print "move ready"
arm.move_ready()
# wait 1 sencond
time.sleep(1)
arm.mode_rmrc()

BasePoint = base_xyzabc[:]
arm.move_rmrc(BasePoint)

raw_input("Start Program!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

StartPoint = [[0.85,0,0.35,0,0,0]]
myPoint3 = StartPoint
for i in np.arange(0,0.55,0.14):
	for j in np.arange(0,0.41,0.15):
		myPoint3.append([0.85 - j, -i, 0.35, 0, 0, 0])

for j in np.arange(0,0.55,0.10):
	myPoint3.append([0.65, - j, 0.45, 0, -33 * toRad, 0])

#for j in range(0,90,10):
	#myPoint3.append([0.55, -0.38, 0.35, -40 * toRad, -j * toRad, 0])
	
Points=Transformation(myPoint3)
f=open("/home/dong/Workspace/dong/DataRecord/Pos.txt","w")

print myPoint3

i=0
j=0
for j in Points:
	print "============================================="
	print i,":",j
#	needReturn = raw_input( "Need return to Start")
#	if needReturn=="y":
#		arm.move_rmrc([0.80, 0, 0.35,0,0,0])
	print "Move to target."
	arm.move_rmrc(j)
	print "Wating for stable."
	time.sleep(6)
	print "Capture Start?"
	tmp=arm.h_FRAME_now*Th2c
	res=[tmp.mat[0]+[tmp.vec[0]]]
	res+=[tmp.mat[1]+[tmp.vec[1]]]
	res+=[tmp.mat[2]+[tmp.vec[2]]]
	res+=[[0,0,0,1]]
	f.writelines([`res`,"\r\n"])
	realsense.save_pointCloud("/home/dong/Workspace/dong/DataRecord/PointCloud_"+str(i)+".pcd")
	#realsense.save_colorImage("/home/dong/Workspace/dong/DataRecord/ColorImage_"+str(i)+".png")
	raw_input("Capture Over!")
	i=i+1
arm.move_rmrc(BasePoint)
f.close()
exit()