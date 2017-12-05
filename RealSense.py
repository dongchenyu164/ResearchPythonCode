#!/usr/bin/env python
# -*- Python -*-
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

#import world path ===================
import WorkspaceDirInfo as shareDir
sys.path.append(shareDir.WorkspaceDir)
import share.tools.geo.geo as geo

#import local path ===================
sys.path.append(os.path.join(".."))
import set_env
baseDir = shareDir.WorkspaceDir + set_env.MyName
sys.path.append(baseDir)
from tools.classes.realsenseClass import realsenseClass
print "initial RealSense"
realsense = realsenseClass()
raw_input("Start to take Background Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

ImageProcess=realsense.imProcess.services["svImProcess"].provided["sv_ip"]

raw_input("Start to take Background Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
ImageProcess.ref.getBackgroundToAlgorithm()
raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
ImageProcess.ref.getEmptyCupToAlgorithm()
CupTop = ImageProcess.ref.getCupRimLevel_InPixle()
print CupTop
raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#print "\r\n\r\n\r\n\r\nLiquidLevel:"
#print ImageProcess.ref.getLiquidLevel_InPixle()
#raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#print "\r\n\r\n\r\n\r\nLiquidLevel:"
#print ImageProcess.ref.getLiquidLevel_InPixle()
#raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#print "\r\n\r\n\r\n\r\nLiquidLevel:"
#print ImageProcess.ref.getLiquidLevel_InPixle()
#raw_input("Start to take EmptyCup Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#print "\r\n\r\n\r\n\r\nLiquidLevel:"
#print ImageProcess.ref.getLiquidLevel_InPixle()
LiquidLevel=-1
DataCount = 0
Filter = [0,0,0,0,0]
while(True):
	time.sleep(0.25)
	print "\r\nGoal:"
	Res = ImageProcess.ref.getLiquidLevel_InPixle()
	
	#if(abs(LiquidLevel-Res)>20 and LiquidLevel!=-1):
		#print "LiquidLevel number ERROR.CONTINUE!!!!"
		#continue
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
		break
	print "\r\nLiquidLevel:"
	print LiquidLevel