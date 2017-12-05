
NeedRealSense = False
import sys
import os
import time
import copy
import threading
import math

import numpy as np

pi = np.pi
toRad=pi/180.0
toDeg=180/pi

def set_tool_xyz(Arm, x=0, y=0, z=0):    
	#time.sleep(0.1)
	
	tool_xyz = [x, -y, z, 0, 0, 0 ]
	Arm.Th2tool = geo.FRAME(xyzabc=[0,0,0.227,0,0,0]) * geo.FRAME(xyzabc=tool_xyz)
	Arm.otc_setToolOffset(xyzabc=Arm.Th2tool.xyzabc())
	time.sleep(0.3)

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
armR = fpa10Class("_l") 

print "mode joint"
armR.mode_joint()
print "move ready"
armR.move_ready()
time.sleep(1)
armR.mode_rmrc()

base =[0.65, 0, 0.25, 0, 0, 0]
base2 =[0.65, 0.3, 0.25, 0, 0, 0]
raw_input("Start Program!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
armR.move_rmrc(base)
#raw_input("Start Program!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#armR.move_rmrc(base2,v_max=0.07)
#raw_input("Start Program!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
times = 1

while(times<21):
	raw_input("==========Start Set Program222!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	set_tool_xyz(armR,0,0,0.06)
	armR.move_rmrc(base)
	print times
	print "==========Set==0,0,0.05========="
	
	set_tool_xyz(armR,0.05,0.05,0.06)
	armR.move_rmrc(base)
	print times
	print "==========Set==0.05,0.05,0.05========="	
	
	set_tool_xyz(armR,0,0,0)
	armR.move_rmrc(base)
	times = times + 1
	
print "Program is finished."