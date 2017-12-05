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

armR = fpa10Class("_r") 
print "mode joint"
armR.mode_joint()
print "move ready"
armR.move_ready()
time.sleep(1)
armR.mode_rmrc()

print "initial RealSense"
#realsense = realsenseClass()
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

#temp=0.34
#i=0
#while temp<0.5:
	#BasePoint =[0.50, 0.0, temp, 0, 0, 0]
	#arm.move_rmrc(BasePoint)
	#realsense.save_pointCloud("./PointCloud_CupBottom_"+str(i)+".pcd")
	#i=i+1
	#temp=temp+0.01
	##realsense.save_colorImage("./ColorImage_"+str(i)+".png")
	#raw_input("Next!!!")


Radius=0.15
Height=0.20

#Xie Fang Xiang1 Second
offset_x=-0.10
offset_y=-0.10
offset_z=0.17
center=[0.80, 0, 0.045]

PosLimit_y = 0.10

step = 0.01
i = 1
myPoint = [Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y, offset_z]),center)]
while (offset_y + i * step) <= PosLimit_y :
	myPoint.append(Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y + i * step, offset_z]),center))
	i = i + 1

#Xie2 Third
offset_x=-0.10
offset_y=0.10
offset_z=0.17
#center=[0.80, 0, 0.045]

PosLimit_x = 0.00###################

#step = 0.01
i = 1
myPoint2 = [Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y, offset_z]),center)]
while (offset_x + i * step) <= PosLimit_x :
	myPoint2.append(Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x + i * step, offset_y, offset_z]),center))
	i = i + 1

#Xie3 First
offset_x=0.0
offset_y=-0.10
offset_z=0.17
#center=[0.80, 0, 0.045]

PosLimit_x = -0.10

#step = 0.01###############
i = 1
myPoint3 = [Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y, offset_z]),center)]
while (offset_x - i * step) >= PosLimit_x :
	myPoint3.append(Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x - i * step, offset_y, offset_z]),center))
	i = i + 1

#Ping Yi
offset_x=-0
offset_y=-0.10
offset_z=0.25
#center=[0.80, 0, 0.045]

PosLimit_y = 0.10

i = 1
Heng = [[0.80, offset_y, offset_z, 0, 0, 0]]
while (offset_y + i * step) <= PosLimit_y :
	Heng.append([0.80, offset_y + i * step, offset_z, 0, 0, 0])
	i = i + 1
myPoint3 = myPoint3+myPoint+myPoint2
Points=Transformation(myPoint3)
f=open("/home/dong/Workspace/dong/DataRecord/Pos.txt","w")

print myPoint3

i=0
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
	realsense.save_colorImage("/home/dong/Workspace/dong/DataRecord/ColorImage_"+str(i)+".png")
#	raw_input("Capture Over!")
	i=i+1
arm.move_rmrc(BasePoint)
f.close()
exit()
