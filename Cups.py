#-*-coding:utf-8-*-

pi=3.14159265358

class CUP:
	DistanceOfRimAndCenter = 0 #出水口到杯子轴心的距离.
	OriginPos=[0,0]
	CenterPos=[0,0]
	High = 0
	HandlePersent = 0.75
	HandlePointHigh = 0
	Rect=[0,0,0]#长宽高 单位:m,杯子的最大外轮廓.
	
	def __init__(self, DistanceOfRimAndCenter = 0.01,CenterPos=[0,0],Rect=[0.07,0.07,0.24],HandlePersent = 1):
		self.DistanceOfRimAndCenter=DistanceOfRimAndCenter
		self.CenterPos=CenterPos
		self.OriginPos=CenterPos
		self.Rect=Rect
		self.High = Rect[2]
		self.HandlePersent = HandlePersent
		
	def GetHandlePoint(self,HandlePersent=1):
		self.HandlePointHigh = self.Rect[2] * HandlePersent
		return [self.CenterPos[0],self.CenterPos[1],self.HandlePointHigh,0,0,0]
	
	def GetRimPosition(self):
		return [self.CenterPos[0],self.CenterPos[1] + DistanceOfRimAndCenter,self.Rect[2],0,0,0]

FirstCup=CUP(0.0435,[0.85,-0.7],[0.122,0.087,0.09],0.85)
SecCup=CUP(0.0415,[0.85,-0.7],[0.083,0.083,0.11],0.80)
GlassMaDoKaCup=CUP(0.0315,[0.85,-0.7],[0.063,0.063,0.11],0.80)
PaperCup=CUP(0.073/2.0,[0.85,-0.6],[0.073,0.073,0.097],0.90)

milkTea=CUP(0.01,[0.85,-0.8],[0.07,0.07,0.24],0.6)

VirtualTarget=CUP(0.0435,[0.70,-0.4],[0.122,0.087,0.09],0.85)