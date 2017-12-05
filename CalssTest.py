import math
pi = 3.14159265358
toRad=pi/180.0
toDeg=180.0/pi
hehe=0
def WatchCup(Direction=180,Distance=0.05,WatchPointHigh=0.25):
	offset_x=math.cos(Direction*toRad) * Distance
	offset_y=-math.sin(Direction*toRad) * Distance
	offset_z=WatchPointHigh
	global hehe
	hehe = [1,2,3]
	print offset_x
	print offset_y
	print offset_z
	
def test():
	global hehe
	tmp = hehe + [0,1.57,0]
	print tmp
WatchCup(-150)
test()

#test=[0.111111,0.222222,0.333333]
#test2=map(round,test,[4]*len(test))
#print test2,round(0.12337,4)
#from Cups import*

#print milkTea.GetHandlePoint(0.6)[0]

#from camera import*

#svppPort=realsense.imProcess.services["svImProcess"].provided["sv_ip"]
#svppPort.ref.getEmptyCupToAlgorithm()
#svppPort.ref.getCupRimLevel_InPixle()

#svppPort.ref.getBackgroundToAlgorithm()
