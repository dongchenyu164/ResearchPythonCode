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
from share.tools.classes.parallelGripperClass import parallelGripperClass

#import local path ===================
sys.path.append(os.path.join(".."))
import set_env
baseDir = shareDir.WorkspaceDir + set_env.MyName
sys.path.append(baseDir)

################initial###########################################
arm = fpa10Class("_l") 


base_xyzabc =[0.65, 0, 0.4, 0, 0, 0]
# change mode joint  and  move ready pose
print "mode joint"
arm.mode_joint()
print "move ready"
arm.move_ready()
# wait 1 sencond
time.sleep(1)
arm.mode_rmrc()

j = base_xyzabc[:]
arm.move_rmrc(j)

print "Start Moving!!!!!!!!!!!!!!!!!!!!!!!!!!!!"



res=ProductPointSequence_Line([0.60,0.10,0.25],[0.60,-0.10,0.25])

res_rotate=ProductPointSequence_Line([0.60,0.10,0.25],[0.60,-0.10,0.25],[0.65,0,0])

print arm.__module__
raw_input("sssssss")
arm.rmrc_MoveByContinuedPointSequence(res_rotate)


