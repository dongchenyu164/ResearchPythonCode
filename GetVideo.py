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
###############

################initial###########################################
print "initial pa10"
arm = fpa10Class("_l") 
print "initial RealSense"
##############################################
print "initial Over"

base_xyzabc =[0.65, 0, 0.20, 0, 0, 0]
# change mode joint  and  move ready pose
print "mode joint"
arm.mode_joint()
print "move ready"
arm.move_ready()
# wait 1 sencond
time.sleep(1)
arm.mode_rmrc()

BasePoint = base_xyzabc[:]
#arm.move_rmrc(BasePoint)

raw_input("Start Program!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

offset_x=-0.05
offset_y=-0.0
offset_z=0.25
center=[0.80, 0, 0.045]

myPoint = [Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y, offset_z]),center)]
Points=Transformation(myPoint)
arm.move_rmrc(Points[0])

f=open("./Pos_Video.txt","w")

i=0	
tmp=arm.h_FRAME_now*Th2c
res=[tmp.mat[0]+[tmp.vec[0]]]
res+=[tmp.mat[1]+[tmp.vec[1]]]
res+=[tmp.mat[2]+[tmp.vec[2]]]
res+=[[0,0,0,1]]
f.writelines([`res`,"\r\n"])
f.close()

raw_input("Move over. Enter to Start RealSense!!!!")

from tools.classes.realsenseClass import realsenseClass
realsense = realsenseClass()

while i < 3000:
	time.sleep(1)
	#Success = False
	#while not Success: 
	realsense.save_pointCloud("./PointCloud_Video"+str(i)+".pcd")
	#Success = False
	#while not Success: 
	realsense.save_irImage("./ColorImage_Video"+str(i)+".png")
	i=i+1
	print i
arm.move_rmrc(BasePoint)
f.close()
exit()
