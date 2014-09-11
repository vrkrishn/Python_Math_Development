import random
import math
from Tkinter import*

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.x) + ")"

class BoundingBox:
	def __init__(self, tl, br):
		self.tl = tl
		self.br = br
		
	def inBounds(self, point):
		return ((point.x >= self.tl.x) and
				(point.x <= self.br.x) and
				(point.y <= self.tl.y) and
				(point.y >= self.br.y))

class ChaosGame:
	
	def __init__(self, bounds, start, r = 0.5):
		self.bounds = bounds
		self.current = start
		self.points = []
		self.r = r
		
	def stepGame(self):
		dest = self.bounds[int(random.random() * len(self.bounds))]
		xSize = abs(dest.x - self.current.x)
		ySize = abs(dest.y - self.current.y)
		xNew = self.current.x + (1 - 2 *(self.current.x > dest.x)) * self.r * xSize
		yNew = self.current.y + (1 - 2 *(self.current.y > dest.y)) * self.r * ySize
		newP = Point(xNew, yNew)
		self.points += [newP]
		self.current = newP

class CoordTransform:
	
	def __init__(self,cHeight,cWidth,xMin,xMax,yMin,yMax):
		self.yInt = cHeight / (yMax - yMin)
		self.xInt = cWidth / (xMax - xMin)
		self.cHeight = cHeight
		self.cWidth = cWidth
		self.xMin = xMin
		self.yMin = yMin
		self.bounds = BoundingBox(Point(xMin,yMax), Point(xMax,yMin))
		
	def MtoV(self,point):
		if (self.bounds.inBounds(point)):
			return Point((point.x - self.xMin) * self.xInt, 
						 self.cHeight - (point.y - self.yMin) * self.yInt)
		else:
			return None
		
class GUI:
	def __init__(self, maxDisplay = 100):
		root = Tk()
		self.canvasWidth = 800
		self.canvasHeight = 800
		canvas = Canvas(root,width=self.canvasWidth,height=self.canvasHeight)
		canvas.pack()
		self.init()#maxDisplay)
		self.timerFired(canvas)
		root.mainloop()
	
	def timerFired(self,canvas):
		self.game.stepGame()
		delay = self.tickPeriod
		self.redrawAll(canvas)
		canvas.after(delay, lambda c=canvas: self.timerFired(c))
	
	def minBoundingBox(self,bounds):
		tl = bounds[0]
		br = bounds[0]
		for point in bounds:
			if point.x < tl.x:
				tl = Point(point.x, tl.y)
			if point.x > br.x:
				br = Point(point.x, br.y)
			if point.y > tl.y:
				tl = Point(tl.x, point.y)
			if point.y < br.y:
				br = Point(br.x, point.y)
		tl = Point(float(int(tl.x)), float(int(tl.y)))
		br = Point(float(int(br.x)), float(int(br.y)))
		return BoundingBox(tl,br)		
	
	def randomStart(self,bounds):
		start = bounds[int(random.random() * len(bounds))]
		count = 0
		while (count < self.seed):
			dest = bounds[int(random.random() * len(bounds))]
			xSize = abs(dest.x - start.x)
			ySize = abs(dest.y - start.y)
			xNew = start.x + (1 - 2 *(start.x > dest.x)) * (random.random()) * xSize
			yNew = start.y + (1 - 2 *(start.y > dest.y)) * (random.random()) * ySize
			start = Point(xNew, yNew)
			count += 1
		xN = 0.0
		yN = 0.0
		return Point(xN, yN)
	
	def init(self):
		self.yMin = 0
		self.yMax = 100
		self.xMin = 0
		self.xMax = 100
		self.tWidth = 5
		self.pRad = .5
		self.tickPeriod = 1
		self.seed = 20
		bounds = [Point(30.0,30.0), Point(70.0, 30.0), Point(70.0,70.0), Point(30.0,70.0)]
		self.box = self.minBoundingBox(bounds)
		start = self.randomStart(bounds)
		ratio = .75
		self.game = ChaosGame(bounds,start, ratio)
		self.CT = CoordTransform(self.canvasHeight, self.canvasWidth,
								 self.xMin, self.xMax, self.yMin, self.yMax)
	
	#canvas goes from -10,10
	def redrawAll(self,canvas):
		canvas.delete(ALL)
		self.drawAxis(canvas)
		self.drawBoundingBox(canvas)
		self.drawPoints(canvas)
		
	def drawAxis(self,canvas):
		yInt = self.canvasHeight / (self.yMax - self.yMin)
		xInt = self.canvasWidth / (self.xMax - self.xMin)
		#vertical axis
		if (0.0 > self.xMin and 0.0 < self.xMax):
			xMid = xInt * (0.0 - self.xMin)
			yMid = yInt * (0.0 - self.yMin)
			canvas.create_line(xMid,0,xMid,self.canvasHeight)
			start = yMid
			while (start > 0):
				canvas.create_line(xMid - self.tWidth, start, xMid + self.tWidth, start)
				start -= yInt
			start = yMid
			while (start < self.canvasHeight):
				canvas.create_line(xMid - self.tWidth, start, xMid + self.tWidth, start)
				start += yInt
		#horizontal axis
		if (0.0 > self.yMin and 0.0 < self.yMax):
			xMid = xInt * (0.0 - self.xMin)
			yMid = yInt * (0.0 - self.yMin)
			canvas.create_line(0,yMid,self.canvasWidth,yMid)
			start = xMid
			while (start > 0):
				canvas.create_line(start, yMid - self.tWidth, start, yMid + self.tWidth)
				start -= xInt
			start = xMid
			while (start < self.canvasHeight):
				canvas.create_line(start, yMid - self.tWidth, start, yMid + self.tWidth)
				start += xInt
	
	def drawBoundingBox(self,canvas):
		tl = self.CT.MtoV(self.box.tl)
		br = self.CT.MtoV(self.box.br)
		canvas.create_line(tl.x, tl.y, tl.x, br.y, fill = "red")
		canvas.create_line(tl.x, tl.y, br.x, tl.y, fill = "red")
		canvas.create_line(br.x, br.y, tl.x, br.y, fill = "red")		
		canvas.create_line(br.x, br.y, br.x, tl.y, fill = "red")		
				
	def drawPoints(self,canvas):
		points = self.game.points
		for p in points:
			guiCoord = self.CT.MtoV(p)
			if (guiCoord != None):
				canvas.create_oval(guiCoord.x - self.pRad, guiCoord.y - self.pRad,
							   	   guiCoord.x + self.pRad, guiCoord.y + self.pRad)
				
	
G = GUI(-1)
		