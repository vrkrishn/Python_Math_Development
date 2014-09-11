import random
from Tkinter import *
import math


def randomPoints(xRange, yRange, numPoints):
	centers = [(random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])) for i in xrange(5)]
	points = []
	for i in xrange(numPoints):
		px = random.randint(xRange[0], xRange[1])
		py = random.randint(yRange[0], yRange[1])
		center = centers[random.randint(0,4)]
		ratio = (4*random.random()/10) + .6
		
		if (center[0] >= px):
			px = px + int(ratio * abs(center[0] - px))
		else:
			px = px - int(ratio * abs(center[0] - px))
			
		if (center[1] >= py):
			py = py + int(ratio * abs(center[1] - py))
		else:
			py = py - int(ratio * abs(center[1] - py))
		
		points.append(Point(px,py))
	return points

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"
		

class MeanPoint(Point):
	def __init__(self, x, y, color):
		self.color = color
		super(MeanPoint, self).__init__(x,y)
		
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
			if (isinstance(point,MeanPoint)):
				result = MeanPoint((point.x - self.xMin) * self.xInt,
						    self.cHeight - (point.y - self.yMin) * self.yInt, point.color)
			else:
				result = Point((point.x - self.xMin) * self.xInt,
						    self.cHeight - (point.y - self.yMin) * self.yInt)
			return result
		else:
			return None


class ClusteringSimulation:
	
	def __init__(self, xRange, yRange, points, k):
		self.xMin = xRange[0]
		self.xMax = xRange[1]
		self.yMin = yRange[0]
		self.yMax = yRange[1]
		self.points = points
		self.k = k
		self.blank = "white"
		r = lambda: random.randint(0,255)
		self.colors = ['#%02X%02X%02X' % (r(),r(),r()) for i in xrange(k)]
		self.kMap = dict()
		
	def kRandomMeans(self):
		return [MeanPoint(random.randint(self.xMin, self.xMax), 
					random.randint(self.yMin, self.yMax), self.colors[i]) for i in xrange(self.k)]
					
	def getClosestData(self, data, means):
		kMap = dict()
		for m in means:
			kMap[m] = []
		for d in data:
			closest = self.closestPoint(d,means)
			kMap[closest] += [d]
		return kMap
	
	def closestPoint(self,target,selection):
		distances = map(lambda p: (p,self.distance(target,p)),selection)
		bestPair = reduce(lambda (pa,d1), (pb,d2): (pa,d1) if d1 < d2 else (pb,d2), distances)
		return bestPair[0]
		
	def distance(self,pa,pb):
		return math.sqrt((pa.x - pb.x)**2 + (pa.y - pb.y)**2)
	
	def getCenters(self, dataMap):
		c = [self.getCenter(dataMap[d]) for d in dataMap]
		return [MeanPoint(c[i].x,c[i].y, self.colors[i]) for i in xrange(len(c))]
	
	def getCenter(self,data):
		if (len(data) == 0):
			return Point(random.randint(self.xMin,self.xMax), random.randint(self.yMin, self.yMax))
		xSum = sum(map(lambda p: p.x, data))
		ySum = sum(map(lambda p: p.y, data))
		return Point(xSum/len(data), ySum/len(data))
		
		
		
class GUI:
	def __init__(self):
		root = Tk()
		self.canvasWidth = 400
		self.canvasHeight = 400
		canvas = Canvas(root,width=self.canvasWidth,height=self.canvasHeight)
		self.canvas = canvas
		canvas.pack()
		self.init()#maxDisplay)
		self.timerFired(canvas)
		root.mainloop()
	
	def timerFired(self,canvas):
		finished = False
		state = self.states[self.currentState]
		if (state == "MEANS"):
			dM = 0
			dC = 0
			for i in xrange(len(self.means)):
				dM += self.means[i].x + self.means[i].y
				dC += self.centers[i].x + self.centers[i].y
			print abs(dM - dC)
			if (abs(dM - dC) <= self.epsilon):
				print "Done"
				finished = True
			self.means = self.centers
			self.centers = []
		elif state == "NEAREST":
			self.dataMap = self.game.getClosestData(self.points, self.means)
		else:
			self.centers = self.game.getCenters(self.dataMap)
		
		if (not finished):		
			self.redrawAll(canvas, state)
			canvas.after(self.tickPeriod, lambda c=canvas: self.timerFired(c))
			self.currentState = (self.currentState + 1) % len(self.states)
	
	def init(self):
		self.lines = [(2,-10)]
		self.yMin = -100
		self.yMax = 100
		self.xMin = -100
		self.xMax = 100
		self.tWidth = 1
		self.tickPeriod = 3000
		self.pRad = .5
		self.CT = CoordTransform(self.canvasHeight, self.canvasWidth,
								 self.xMin, self.xMax, self.yMin, self.yMax)
		
		numPoints = 1000
		k = 5			 
		self.points = randomPoints((self.xMin,self.xMax), (self.yMin, self.yMax), numPoints)
		self.game = ClusteringSimulation((self.xMin, self.xMax), (self.yMin, self.yMax), self.points, k)
		self.means = self.game.kRandomMeans()
		self.centers = self.game.kRandomMeans()	
		self.dataMap = None	 
		self.states = ["MEANS", "NEAREST", "CENTER"]
		self.currentState = 0;			 
		self.epsilon = 1
			
	#canvas goes from -10,10
	def redrawAll(self,canvas,state):
		if state == "CENTER":
			for c in self.centers:
				self.drawPoint(canvas, c.x,c.y, 8*self.pRad, "green")
		elif state == "MEANS":
			canvas.delete(ALL)
			self.drawAxis(canvas)
			for p in self.points:
				self.drawPoint(canvas, p.x, p.y, self.pRad, "black")
			for m in self.means:
				self.drawPoint(canvas, m.x,m.y, 8*self.pRad, "red")
			
		else:
			canvas.delete(ALL)
			means = map(lambda p: self.CT.MtoV(p),self.means)
			for row in xrange(self.canvasHeight):
				for col in xrange(self.canvasWidth):
					closest = self.game.closestPoint(Point(col,row), means)
					canvas.create_rectangle(col,row,col+1,row+1, width=0, fill = closest.color)
					
			self.drawAxis(canvas)
			for p in self.points:
				self.drawPoint(canvas, p.x, p.y,self.pRad, "black")
			for m in self.means:
				self.drawPoint(canvas, m.x,m.y, 8*self.pRad, "red")
		
	def drawPoint(self,canvas, x, y, pRad, color = "black"):
		guiCoord = self.CT.MtoV(Point(x,y))
		if (guiCoord != None):
			canvas.create_oval(guiCoord.x - pRad, guiCoord.y - pRad,
							   guiCoord.x + pRad, guiCoord.y + pRad, fill = color, width = 0)
						
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
