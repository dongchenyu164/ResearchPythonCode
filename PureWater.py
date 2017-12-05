#!/usr/bin/env python
# -*- Python -*-

NeedRealSense = False

#Initial
if True:
	import sys
	import os
	import time
	import copy
	import threading
	import math
	
	import GlobeVars
	from Algorithm import*
	from Cups import*
	import numpy as np
	
	pi = np.pi
	toRad=pi/180.0
	toDeg=180/pi
	
	def set_tool_xyz(Arm, x=0, y=0, z=0):    
		tool_xyz = [x, -y, z, 0, 0, 0 ]
		Arm.Th2tool = geo.FRAME(xyzabc=[0,0,0.227,0,0,0]) * geo.FRAME(xyzabc=tool_xyz)
		Arm.otc_setToolOffset(xyzabc=Arm.Th2tool.xyzabc())
	
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
	if NeedRealSense:
		from tools.classes.realsenseClass import realsenseClass
	
	
	
	################initial###########################################
	print "initial pa10"
	#armR = fpa10Class("_r") 
	#armL = fpa10Class("_l") 
	print "initial Gripper"
	GlobeVars.Gripper = parallelGripperClass("_r")
	
	GripperL = parallelGripperClass("_l")
	GlobeVars.Gripper.parallelGripper_free()
	GripperL.parallelGripper_free()
	
	if NeedRealSense:
		print "initial RealSense"
		realsense = realsenseClass()
		ImageProcess=realsense.imProcess.services["svImProcess"].provided["sv_ip"]
	print "initial Over"
	
	#raw_input("Start Program000!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	base_xyzabc =[0.65, 0, 0.20, 0, 0, 0]
	print "mode joint"
	armL.mode_joint()
	print "move ready"
	armL.move_ready()
	time.sleep(1)
	armL.mode_rmrc()
	
	#raw_input("Stop Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	#armR.mode_rmrc()
	#tmp = map(lambda x,y:x+y, armR.t_FRAME_now.xyzabc(), [0,0,0.1,0,0,0])
	#armR.move_rmrc(tmp)
	
	print "mode joint"
	armR.mode_joint()
	print "move ready"
	armR.move_ready()
	time.sleep(1)
	armR.mode_rmrc()
	#raw_input("Stop Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	#armR.move_rmrc([0.75,-0.7,0.17,0,-90*toRad,0])
	CoordForArmR = [0,0.8,0,0,0,0]
	armR.coordMode_Table(CoordForArmR)

from Actions import*
WatchPoint = [0.70,-0.4]


#raw_input("Start WatchCup() Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#WatchCup(armL,WatchPoint,-135)

#raw_input("Start to take Background Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#ImageProcess.ref.getBackgroundToAlgorithm()

#raw_input("Start to move ready Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#armL.move_ready()

raw_input("Start MoveObjTo_FromUp() Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
MoveObjTo_FromUp(armR,PaperCup,WatchPoint,Force=77)
#raw_input("Start to MoveRealsense to Watch Point Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#WatchCup(armL,WatchPoint,-135)
#raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#ImageProcess.ref.getEmptyCupToAlgorithm()
#CupTop = ImageProcess.ref.getCupRimLevel_InPixle()
#print CupTop

raw_input("Start to take Pour Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
PrePourAction(armR,milkTea,PaperCup)#tool坐标系回退4cm.

LiquidLevel=-1
PourOver=False
DataCount = 0
Filter = [0,0,0,0,0]

def LiquidLevelDetect_ThreadProcess():
	global ImageProcess, LiquidLevel, CupTop, PourOver, DataCount, Filter

	while(True):
		time.sleep(0.25)
		print "\r\nGoal:"
		Res = ImageProcess.ref.getLiquidLevel_InPixle()

		if(Res==-1):
			print "Get LiquidLevel ERROR.CONTINUE!!!!"
			continue
	
		DataCount=DataCount+1
		Filter[DataCount%5] = Res
		if(DataCount<=5):
			continue
		LiquidLevel = average(Filter)
	
		print LiquidLevel - CupTop
		if(abs(LiquidLevel - CupTop) < 80):
			PourOver = True
			print "\r\nExit!!!!!!!!!!!!!!!!!!!!"
			return
		print "\r\nLiquidLevel:"
		print LiquidLevel
		
def PourAngleControl_ThreadProcess():
	global armR
	AddPourAngle(armR,-26*toRad)
	
import threading
LiquidLevelDetect_Thread = threading.Thread(target = LiquidLevelDetect_ThreadProcess)
#PourAngleControl_Thread = threading.Thread(target = PourAngleControl_ThreadProcess)
LiquidLevelDetect_Thread.setDaemon(True)
#PourAngleControl_Thread.setDaemon(True)
raw_input("Start LiquidLevelDetect_Thread!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
LiquidLevelDetect_Thread.start()
#PourAngleControl_Thread.start()

raw_input("Start Pour!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
AddPourAngle(armR,-25*toRad)
while (PourOver == False):
	time.sleep(0.05)
	continue
print "Stop Pour!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
StopPour(armR,milkTea)
armL.move_ready()
raw_input("Stop Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#PrePourAction(armR,milkTea,PaperCup)#tool坐标系回退4cm.

#AddPourAngle(armR)
#AddPourAngle(armR)
#AddPourAngle(armR)
#AddPourAngle(armR,-30*toRad)
#AddPourAngle(armR,-30*toRad)
#AddPourAngle(armR)
#AddPourAngle(armR)
#raw_input("Start Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#StopPour(armR,milkTea)

#WatchCup(armL,WatchPoint)
#raw_input("Stop Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#armL.move_ready()
#raw_input("Stop Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

