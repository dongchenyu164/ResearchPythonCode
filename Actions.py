#-*-coding:utf-8-*-

import time
import GlobeVars
from Algorithm import*
from Cups import*
import numpy as np

pi = np.pi
toRad=pi/180.0
toDeg=180.0/pi

def set_tool_xyz(Arm, x=0, y=0, z=0):    
	tool_xyz = [x, -y, z, 0, 0, 0 ]
	Arm.Th2tool = geo.FRAME(xyzabc=[0,0,0.227,0,0,0]) * geo.FRAME(xyzabc=tool_xyz)
	Arm.otc_setToolOffset(xyzabc=Arm.Th2tool.xyzabc())
	time.sleep(0.5)

def _CatchObjFromBack(Arm, Obj, Force = 140):
	#Diff=map(lambda x,y:x-y,HandPosition,PointPosition)
	CupHandlePoint = Obj.GetHandlePoint(Obj.HandlePersent)
	
	Arm.move_rmrc(map(lambda x,y:x+y,CupHandlePoint,[-0.2,0,0,0,0,0]) ,DEBUG_MSG = "CatchObjFromBack 移动至物体后20cm")#移动至物体后20cm.
	Arm.move_rmrc(map(lambda x,y:x+y,CupHandlePoint,[-0.2,0,0,0,-40*toRad,0]) ,DEBUG_MSG = "CatchObjFromBack 先使手臂后倾40度")#先使手臂后倾40度.
	
	GlobeVars.Gripper.parallelGripper_open(140)#打开抓手.
	time.sleep(2)	
	Arm.move_rmrc(map(lambda x,y:x+y,CupHandlePoint,[0,0,0,0,-90*toRad,0]) ,DEBUG_MSG = "CatchObjFromBack 使手臂倾至90度")#使手臂倾至90度.
	#GlobeVars.Gripper.parallelGripper_free()#放松抓手.
	
	GlobeVars.Gripper.parallelGripper_close(Force)#闭合抓手.	
	time.sleep(2)
def _CatchObjFromUp(Arm, Obj, Force = 140):
	#Diff=map(lambda x,y:x-y,HandPosition,PointPosition)
	CupHandlePoint = Obj.GetHandlePoint(Obj.HandlePersent)

	Arm.move_rmrc(map(lambda x,y:x+y,CupHandlePoint,[0,0,0.1,0,0,0]) ,DEBUG_MSG = "CatchObjFromUp 移动至物体上10cm")#移动至物体后20cm.

	GlobeVars.Gripper.parallelGripper_open(140)#打开抓手.
	time.sleep(2)	
	Arm.move_rmrc(map(lambda x,y:x+y,CupHandlePoint,[0,0,0,0,0,0]) ,DEBUG_MSG = "CatchObjFromUp 移动至物体上")#使手臂倾至90度.

	GlobeVars.Gripper.parallelGripper_close(Force)#闭合抓手.	
	raw_input("Closed???????")
	#time.sleep(2)	
	
def _MoveTo(Arm, Pos=[0.75,-0.4], Rotate = 0, High = 0.05):
	tmp = map(lambda x,y:x+y, Arm.t_FRAME_now.xyzabc(), [0,0,High,0,0,0])
	Arm.move_rmrc(tmp ,DEBUG_MSG = "MoveTo 拿起来")#拿起来.
	Arm.move_rmrc([Pos[0],Pos[1],tmp[2],		0,-90*toRad,Rotate] ,DEBUG_MSG = "MoveTo 移动")#移动.
	Arm.move_rmrc([Pos[0],Pos[1],tmp[2] - High,	0,-90*toRad,Rotate] ,DEBUG_MSG = "MoveTo 放下")#.
def _MoveToFromUp(Arm, Pos=[0.75,-0.4], Rotate = 0, High = 0.05):
	tmp = map(lambda x,y:x+y, Arm.t_FRAME_now.xyzabc(), [0,0,High,0,0,0])
	Arm.move_rmrc(tmp ,DEBUG_MSG = "MoveToFromUp 拿起来")#拿起来.
	Arm.move_rmrc([Pos[0],Pos[1],tmp[2],		0,0,Rotate] ,DEBUG_MSG = "MoveToFromUp 移动")#移动.
	Arm.move_rmrc([Pos[0],Pos[1],tmp[2] - High,	0,0,Rotate] ,DEBUG_MSG = "MoveToFromUp 放下")#.	
def _MoveTo_3D(Arm, Pos=[0.75,-0.4,0.25], Rotate = 0, High = 0.05):
	tmp = map(lambda x,y:x+y, Arm.t_FRAME_now.xyzabc(), [0,0,High,0,0,0])
	Arm.move_rmrc(tmp ,DEBUG_MSG = "MoveTo_3D 拿起来")#拿起来.
	Arm.move_rmrc([Pos[0],Pos[1],Pos[2],0,-90*toRad,Rotate] ,DEBUG_MSG = "MoveTo_3D 移动")#移动.	
	
def _ReleaseObjAndReturnArm(Arm, Obj):
	GlobeVars.Gripper.parallelGripper_open(140)#打开抓手.
	time.sleep(2)
	tmp = Arm.t_FRAME_now.xyzabc()
	tmp[2] = Obj.High + 0.1
	Arm.move_rmrc(tmp ,DEBUG_MSG = "ReleaseObj 上移10cm")
	GlobeVars.Gripper.parallelGripper_free()#放松抓手.
	
	Arm.move_ready()
		
def MoveObjTo(Arm,Obj, TargetPos=[0.75,-0.4], Rotate = 0, Force = 140):
	_CatchObjFromBack(Arm, Obj, Force = Force)
	_MoveTo(Arm,[TargetPos[0],TargetPos[1]],Rotate)
	_ReleaseObjAndReturnArm(Arm,Obj)
	Obj.CenterPos = TargetPos
def MoveObjTo_FromUp(Arm,Obj, TargetPos=[0.75,-0.4], Rotate = 0, Force = 140):
	_CatchObjFromUp(Arm, Obj, Force = Force)
	_MoveToFromUp(Arm,[TargetPos[0],TargetPos[1]],Rotate)
	_ReleaseObjAndReturnArm(Arm,Obj)
	Obj.CenterPos = TargetPos
def MoveObjTo_3D(Arm,Obj, TargetPos=[0.75,-0.4,0.25], Rotate = 0, Force = 140):
	_CatchObjFromBack(Arm, Obj, Force = Force)
	_MoveTo_3D(Arm,[TargetPos[0],TargetPos[1],TargetPos[2]],Rotate)
	Obj.CenterPos = TargetPos

gPrePos = 0
def PrePourAction(Arm,OriginObj,TargetObj, ReadyAngle = -60 * toRad, Force = 140):
	set_tool_xyz(Arm,0,0,-0.04)
	tmp = Arm.t_FRAME_now.xyzabc()
	PrePos = [TargetObj.CenterPos[0],TargetObj.CenterPos[1] + (-TargetObj.DistanceOfRimAndCenter-OriginObj.Rect[1]),tmp[2]]
	#PrePos有时候回算成负的.....
	TargetPos = [TargetObj.CenterPos[0],TargetObj.CenterPos[1] + (-TargetObj.DistanceOfRimAndCenter*0.45),TargetObj.High*1.5]
	print "PrePourAction-MoveObjTo_3D"
	MoveObjTo_3D(Arm, OriginObj, PrePos, Force = Force)
	Arm.move_rmrc(PrePos + [ReadyAngle,-90*toRad,0])
	
	NewAxis=[OriginObj.High - OriginObj.HandlePointHigh,OriginObj.DistanceOfRimAndCenter,-0.04]
	print NewAxis
	set_tool_xyz(Arm,NewAxis[0],NewAxis[1],NewAxis[2])
	set_tool_xyz(Arm,NewAxis[0],NewAxis[1],NewAxis[2])
	Arm.move_rmrc(TargetPos + [ReadyAngle,-90*toRad,0])
	#tmp = map(lambda x,y:x+y, Arm.t_FRAME_now.xyzabc(), [0,0,0,ReadyAngle,0,0])
	#Arm.move_rmrc(tmp ,DEBUG_MSG = "PrePourAction To Ready Angle")
	global gPrePos
	gPrePos = PrePos
	return True
def AddPourAngle(Arm,Step = -10 * toRad):
	tmp = Arm.t_FRAME_now.xyzabc()
	print tmp[5] * toDeg
	print tmp[4] * toDeg
	print tmp[3] * toDeg
	if((tmp[3] * toDeg + Step * toDeg) < -150):
		tmp[3] = -150 * toRad
		Arm.move_rmrc(tmp ,DEBUG_MSG = "AddPourAngle at Max 限幅150度")
	else:#t_FRAME_now.xyzabc()这个跟rmrc的坐标轴对不上....
		tmp = map(lambda x,y:x+y, Arm.t_FRAME_now.xyzabc(), [0,0,0,Step,0,0])
		Arm.move_rmrc(tmp ,DEBUG_MSG = "AddPourAngle 限幅150度" + str(tmp[3]*toDeg))
def StopPour(Arm,OriginObj):
	set_tool_xyz(Arm,0,0,-0.04)
	set_tool_xyz(Arm,0,0,-0.04)
	global gPrePos
	tmp = gPrePos + [0,-90*toRad,0]###########################################
	Arm.move_rmrc(tmp ,DEBUG_MSG = "StopPour")
	tmp = [OriginObj.OriginPos[0],OriginObj.OriginPos[1],OriginObj.HandlePointHigh]+[0,-90*toRad,0]
	Arm.move_rmrc(tmp ,DEBUG_MSG = "StopPour Move To Origin Point")
	_ReleaseObjAndReturnArm(Arm,OriginObj)
	return True

#Direction 单位是角度(顺时针为正角度(Realsense从后面看为180度)) Distance 监视点到目标点的水平距离
def WatchCup(ArmWithRealSense, Cup, Direction = 180, Distance = 0.08, WatchPointHigh = 0.25):
	offset_x=math.cos(Direction * toRad) * Distance
	offset_y=-math.sin(Direction * toRad) * Distance
	offset_z=WatchPointHigh
	centerHigh = 0.045
	if(isinstance(Cup,list)):
		center=[Cup[0], Cup[1], centerHigh]
	else:
		center=[Cup.CenterPos[0], Cup.CenterPos[1], centerHigh]
		
	myPoint = [Cal_HandDirect_PointTo(map(lambda x,y:x+y,center,[offset_x, offset_y, offset_z]),center)]
	Points=Transformation(myPoint)
	
	ArmWithRealSense.move_rmrc(Points[0] ,DEBUG_MSG = "看杯子")	
	