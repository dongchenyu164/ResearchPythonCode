# coding=utf-8

import sys
import math

#import world path ===================
import WorkspaceDirInfo as shareDir
sys.path.append(shareDir.WorkspaceDir)

import share.tools.geo.geo as geo
pi=3.14159265358
toRad=pi/180.0
toDeg=180/pi

#=======================================================================
#This function is calculate the hand direction that hand point to the point that you want to point.

#PointPosition:The Point that you want robot hand want to point.

#Caution:HandPosition and PointPosition is in the same coordinate.
#=======================================================================#
def Cal_HandDirect_PointTo(HandPosition,PointPosition,isNeedCal=True):
	#Calculate the each differences between HandPosition and PointPosition
	#next segment is same as 
	#Diff[0]=HandPosition[0]-PointPosition[0]
	#Diff[1]=HandPosition[1]-PointPosition[1]
	#Diff[2]=HandPosition[2]-PointPosition[2]
	#this three segments.
	if isNeedCal:
		if(isinstance(HandPosition[0],float)):
			Diff=map(lambda x,y:x-y,HandPosition,PointPosition)

			#using atan2 is more safer than atan. But atan2's parameters is different from atan.
			#Alpha=-math.atan(Diff[1]/Diff[2])
			#Beta=math.atan(Diff[0]/Diff[2])
			#Gamma=math.atan(Diff[1]/Diff[0])
			Alpha=math.atan2(-Diff[1],Diff[2])
			Beta=math.atan2(Diff[0],Diff[2])
			Gamma=math.atan2(-Diff[1],-Diff[0])

			return [HandPosition[0],HandPosition[1],HandPosition[2],Alpha,Beta,Gamma]
		elif(isinstance(HandPosition[0],list)):
			Res = [None]*len(HandPosition) 

			for i in range(0,len(HandPosition)):
				Diff=map(lambda x,y:x-y,HandPosition[i],PointPosition)

				Alpha=math.atan2(-Diff[1],Diff[2])
				Beta=math.atan2(Diff[0],Diff[2])
				Gamma=math.atan2(-Diff[1],-Diff[0])

				Res[i] = [0]*3 
				Res[i]=[HandPosition[i][0],HandPosition[i][1],HandPosition[i][2],Alpha,Beta,Gamma]
			return Res
	else:
		return [HandPosition[0],HandPosition[1],HandPosition[2],0,0,0]
#=======================================================================#

#=======================================================================#
def ProductPointSequence_Line(Start,End,PointPosition=[0],Interval=0.0001):
	if (len(PointPosition) != 3 and len(PointPosition) != 1) :
		return "Length of PointPosition is not 3 or 1."	
	if (len(Start) != 3) :
		return "Length of PointPosition is not 3."	
	if (len(End) != 3) :
		return "End"

	#
	Diff=map(lambda x,y:(x-y)*1,End,Start)
	Length=math.sqrt(Diff[0]*Diff[0]+Diff[1]*Diff[1]+Diff[2]*Diff[2])
	Delta=map(lambda x:x/(Length/Interval),Diff)

	Res=[[0 for col in range(3)] for row in range(int(Length/Interval))]

	if PointPosition==[0] :
		tmpArray=[False for row in range(int(Length/Interval))]
	else:
		PointPosition=[PointPosition for row in range(int(Length/Interval))]

	for i in range(0,int(Length/Interval)):
		Res[i]=map(lambda x,y:x+y,Start,[x * i for x in Delta])

	if PointPosition==[0] :
		return map(Cal_HandDirect_PointTo,Res,Res,tmpArray)
	else:
		return map(Cal_HandDirect_PointTo,Res,PointPosition)
#=======================================================================#

#=======================================================================#
def GetPhotoPoint(Radius,Height,ThingsPoint):
	tmp = [None]*10
	for i in range(len(tmp)):  
		tmp[i] = [0]*3  

	tmp[0]=[ThingsPoint[0]-Radius,ThingsPoint[1],Height]
	#tmp[0]=[ThingsPoint[0]+Radius,ThingsPoint[1],Height]#这个位置把固定RealSence的板子给折了.....
	tmp[3]=[ThingsPoint[0]-Radius,ThingsPoint[1],Height]
	tmp[1]=[ThingsPoint[0]+Radius/2,ThingsPoint[1]-Radius*math.sqrt(3)/2,Height]
	tmp[2]=[ThingsPoint[0]-Radius/2,ThingsPoint[1]-Radius*math.sqrt(3)/2,Height]
	tmp[4]=[ThingsPoint[0]-Radius/2,ThingsPoint[1]+Radius*math.sqrt(3)/2,Height]
	tmp[5]=[ThingsPoint[0]+Radius/2,ThingsPoint[1]+Radius*math.sqrt(3)/2,Height]

	tmp[6]=[ThingsPoint[0] + Radius/2*math.sqrt(2)/2,ThingsPoint[1] + Radius/2*math.sqrt(2)/2,Height*2]
	tmp[7]=[ThingsPoint[0] + Radius/2*math.sqrt(2)/2,ThingsPoint[1]-Radius/2*math.sqrt(2)/2,Height*2]
	tmp[8]=[ThingsPoint[0]-Radius/2*math.sqrt(2)/2,ThingsPoint[1]-Radius/2*math.sqrt(2)/2,Height*2]
	tmp[9]=[ThingsPoint[0]-Radius/2*math.sqrt(2)/2,ThingsPoint[1] + Radius/2*math.sqrt(2)/2,Height*2]

	return Cal_HandDirect_PointTo(tmp,ThingsPoint)
#=======================================================================#

#=======================================================================#
def Transformation(HandPose,CameraPose = [0.085,0,0.08,0,0,0*toRad]):#This Function can not process with angle.
	tmp= map(lambda x:-x,CameraPose)
	camPose=geo.FRAME(xyzabc = tmp)
	if(isinstance(HandPose[0],list)):#For serial of Poses
		Res = [[0 for col in range(6)] for row in range(len(HandPose))]	
		for i in range(0,len(HandPose)):
			Res[i][:3] = (geo.FRAME(xyzabc = HandPose[i])*camPose).vec
			Res[i][3:] = map(lambda x,y:x+y,HandPose[i][3:],tmp[3:])
		return Res
	elif(isinstance(HandPose,list) and len(HandPose) == 6):#For single Pose.
		Res = [0 for col in range(6)]
		Res[:3] = ((geo.FRAME(xyzabc = HandPose))*camPose).vec
		Res[3:] = map(lambda x,y:x+y,HandPose[3:],tmp[3:])
		return Res
	return False
#=======================================================================#

#=======================================================================#
def average(seq): 
	return float(sum(seq)) / len(seq)

def average_WithoutMaxMin(seq): 
	return float(sum(seq)-max(seq)-min(seq)) / (len(seq) - 2)