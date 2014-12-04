import random
import math

import sys
sys.path.append('../tools')
from gui_util import *

class ChaosGame(Simulation):
	
	def __init__(self, xMin, xMax, yMin, yMax, corners, start, maxPoints, r = 0.5):
		super(ChaosGame, self).__init__(xMin, xMax, yMin, yMax)
		self.maxPoints = maxPoints
		self.corners a= corners
		self.current = start
		self.r = r
		self.points = []

	def step(self):
		dest = self.corners[int(random.random() * len(self.corners))]
		xSize = abs(dest.x - self.current.x)
		ySize = abs(dest.y - self.current.y)
		xNew = self.current.x + (1 - 2 *(self.current.x > dest.x)) * self.r * xSize
		yNew = self.current.y + (1 - 2 *(self.current.y > dest.y)) * self.r * ySize
		newP = Point(xNew, yNew)
		self.points += [newP]
		self.current = newP
		if (len(self.points) >= self.maxPoints):
			return ("FINISHED", newP)
		else:
			return ("IN_PROGRESS", newP)

class ChaosGUI(GUI):
	
	def __init__(self, canvasWidth, canvasHeight, maxDisplay = 1000):
		xMin = 0
		xMax = 100
		yMin = 0
		yMax = 100
		
		bounds = [Point(20,20), Point(20,80), Point(80,20), Point(80,80)]
		self.box = self.minBoundingBox(bounds)
		self.initialized = False
		
		start = Point(50,50)
		
		game = ChaosGame(0, 100, 0, 100, bounds, start, maxDisplay, 0.5)
		super(ChaosGUI, self).__init__(False, canvasWidth, canvasHeight, game, 10)
		
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
		return Rect(tl,br)
		
	def drawBoundingBox(self,canvas, box):
		tl = self.CT.MtoV(box.tl)
		br = self.CT.MtoV(box.br)
		canvas.create_line(tl.x, tl.y, tl.x, br.y, fill = "red")
		canvas.create_line(tl.x, tl.y, br.x, tl.y, fill = "red")
		canvas.create_line(br.x, br.y, tl.x, br.y, fill = "red")		
		canvas.create_line(br.x, br.y, br.x, tl.y, fill = "red")
	
	def redrawAll(self, canvas, output):
		if (output[0] == "FINISHED"):
			return
		
		if (self.initialized == False):
			super(ChaosGUI, self).redrawAll(can  gx
			 b vas, output)
			self.drawBoundingBox(canvas, self.box)
			self.initialized = True
		else:
			self.drawPoint(canvas, output[1], 1, "black")
			
C = ChaosGUI(400, 400)