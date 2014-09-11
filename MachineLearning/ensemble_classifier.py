import random
import math
from Tkinter import *

def randomPoints(xRange, yRange, numPoints):
	points = []
	for i in xrange(numPoints):
		px = random.randint(xRange[0], xRange[1])
		py = random.randint(yRange[0], yRange[1])
		points.append((px,py))
	return points
	
def bestFitLine(points):
	xList = [point[0] for point in points]
	yList = [point[1] for point in points]
	xM = sum(xList)/float(len(xList))
	yM = sum(yList)/float(len(yList))
	xS = sum(map(lambda x: x*x, xList))
	xy = sum(map(lambda i: xList[i] * yList[i], range(len(points))))
	topM = xy - (sum(xList)*sum(yList)/float(len(points)))
	botM = xS - (sum(xList)**2)/float(len(points))
	m = topM / botM
	b = yM - m*xM
	return (m,b)
	
def randomSubset(a,k):
	return random.sample(a, k)
	
def ensembleClassify(points, trees, depth):
	arrays = [random.sample(points, depth) for i in range(trees)]
	return map(lambda points: bestFitLine(points), arrays)
	
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"
		

class BoundingBox:
	def __init__(self, tl, br):
		self.tl = tl
		self.br = br
		
	def inBounds(self, point):
		return ((point.x >= self.tl.x) and
				(point.x <= self.br.x) and
				(point.y <= self.tl.y) and
				(point.y >= self.br.y))

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
			result = Point((point.x - self.xMin) * self.xInt,
						    self.cHeight - (point.y - self.yMin) * self.yInt)
			return result
		else:
			return None

class GUI:
	def __init__(self):
		root = Tk()
		self.canvasWidth = 800
		self.canvasHeight = 800
		canvas = Canvas(root,width=self.canvasWidth,height=self.canvasHeight)
		self.canvas = canvas
		canvas.pack()
		self.init()#maxDisplay)
		self.redrawAll(canvas)
		root.mainloop()
	
	def init(self):
		self.lines = [(2,-10)]
		self.yMin = -100
		self.yMax = 100
		self.xMin = -100
		self.xMax = 100
		self.tWidth = 1
		self.tickPeriod = 1
		self.pRad = .5
		self.CT = CoordTransform(self.canvasHeight, self.canvasWidth,
								 self.xMin, self.xMax, self.yMin, self.yMax)
								 			 
		numPoints = 10000	
		trees = 100
		depth = 10			 
		self.points = randomPoints((self.xMin,self.xMax), (self.yMin, self.yMax), numPoints)
		self.bestFit = bestFitLine(self.points)
		self.treeFits = ensembleClassify(self.points, trees, depth)
		yInts = [tree[1] for tree in self.treeFits]
		slopes = [tree[0] for tree in self.treeFits]
		self.estimatedFit = (sum(slopes)/float(len(self.treeFits)),sum(yInts)/float(len(self.treeFits)))
			
			
	#canvas goes from -10,10
	def redrawAll(self,canvas):
		canvas.delete(ALL)
		self.drawAxis(canvas)
		for (x,y) in self.points:
			self.drawPoint(canvas, x, y)
			
		for (m,b) in self.treeFits:
			self.drawLine(m,b, canvas, "grey")
			
		self.drawLine(self.bestFit[0], self.bestFit[1], canvas, "blue")
		self.drawLine(self.estimatedFit[0], self.estimatedFit[1], canvas, "red")
		
	def drawPoint(self,canvas, x, y):
		guiCoord = self.CT.MtoV(Point(x,y))
		if (guiCoord != None):
			canvas.create_oval(guiCoord.x - self.pRad, guiCoord.y - self.pRad,
							   guiCoord.x + self.pRad, guiCoord.y + self.pRad)
	
	def drawLine(self, m,b, canvas,color = "red"):
		yIntMin = m * self.xMin + b
		yIntMax = m * self.xMax + b
		xIntMin = (self.yMin - b)/m
		xIntMax = (self.yMax - b)/m
		
		points = []
		if (yIntMin >= self.yMin and yIntMin < self.yMax):
			points += [(self.xMin,yIntMin)]
		if (yIntMax >= self.yMin and yIntMax < self.yMax):
			points += [(self.xMax,yIntMax)]
		if (xIntMin >= self.xMin and xIntMin < self.xMax):
			points += [(xIntMin,self.yMin)]
		if (xIntMax >= self.xMin and xIntMax < self.xMax):
			points += [(xIntMax,self.yMax)]
		
		if (len(points) == 2):
			bound_A = self.CT.MtoV(Point(points[0][0], points[0][1]))
			bound_B = self.CT.MtoV(Point(points[1][0], points[1][1]))
			canvas.create_line(bound_A.x, bound_A.y, bound_B.x, bound_B.y, fill=color)
						
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
				
G = GUI()