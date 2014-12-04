import random
import math

import sys
sys.path.append('../tools')
from gui_util import *

class MeanShiftSimulation(Simulation):
	
	def __init__(self, xRange, yRange, points, bandwidth, stopThresh): 
		xMin = xRange[0] 
		xMax = xRange[1] 
		yMin = yRange[0] 
		yMax = yRange[1]
		
		super(MeanShiftSimulation, self).__init__(xMin, xMax, yMin, yMax)
		
		self.points = points 
		self.cand_ind = 0 
		self.candidate = self.points[0] 
		self.n_points = len(points)
		self.currentState = 0 
		self.newMean = None 
		self.currentState = "GET_NEIGHBORS" 
		self.centers = [] 
		self.assignment = [0 for i in xrange(self.n_points)] 
		self.bandwidth = bandwidth 
		self.stopThresh = stopThresh 
		self.distance = lambda pa, pb: math.sqrt((pa.x - pb.x)**2 + (pa.y - pb.y)**2) 
		#self.distance = lambda pa, pb: abs(pa.x - pb.x) + abs(pa.y - pb.y)

	def step(self):
		if (self.currentState == "GET_NEIGHBORS"): 
			self.currentState = "FIND_MEAN" 
			self.neighbors = self.getSurroundingPoints(self.candidate, self.bandwidth) 
			return ["GET_NEIGHBORS", self.candidate, self.neighbors] 
			
		elif (self.currentState == "FIND_MEAN"): 
			self.newMean = self.getCenter(self.neighbors)
			self.currentState = "UPDATE_MEAN" 
			return ["FIND_MEAN", self.newMean] 
			
		elif (self.currentState == "UPDATE_MEAN"):
			delta = self.distance(self.newMean, self.candidate)
			
			self.candidate = self.newMean 
			
			if (delta <= self.stopThresh):
				new_center = True 
				
				#check if there is an existing center within the absorb threshold of candidate
				for c in xrange(len(self.centers)):
					if self.distance(self.centers[c],self.newMean) <= 2 * self.stopThresh: 
						new_center = False 
						self.assignment[self.cand_ind] = c 
						break
				
				#If we have to create a new center, do so	
				if (new_center):
					self.centers += [self.newMean] 
					self.assignment[self.cand_ind] = len(self.centers) - 1
				
				
				self.cand_ind = self.cand_ind + 1
				
			if (self.cand_ind >= self.n_points): 
				self.currentState = "FINISHED" 
			else: 
				self.currentState = "GET_NEIGHBORS" 
				if (delta <= self.stopThresh):
					self.candidate = self.points[self.cand_ind]
			
			return ["UPDATE_MEAN", self.newMean]
			
		else:
			print self.assignment
			return ["FINISHED", self.centers, self.assignment]
						
	def getCenter(self,data):
		if (len(data) == 0): 
			return data 
		xSum = sum(map(lambda p: p.x, data)) 
		ySum = sum(map(lambda p: p.y, data)) 
		return Point(xSum/len(data), ySum/len(data))
		
	def getSurroundingPoints(self, base, bandwidth):
		return filter(lambda p: self.distance(base, p) < bandwidth, self.points)
		
class MeanShiftGUI(GUI):
	def __init__(self, disable_high_gui, canvasWidth, canvasHeight):
		self.cWidth = 800
		self.cHeight = 800
		numPoints = 250
		
		yMin = -100
		yMax = 100
		xMin = -100
		xMax = 100
		
		stats  =  randomPoints((xMin, xMax), (yMin,  yMax),  numPoints,  15)
		self.points = stats[0]
		self.bandwidth = 20
		thresh = 1
		
		self.pRad = 1
		
		game = MeanShiftSimulation((xMin, xMax), (yMin, yMax), self.points, self.bandwidth, thresh)
		
		super(MeanShiftGUI, self).__init__(False, canvasWidth, canvasHeight, game, 1)
            
	#canvas goes from -10,10
	def redrawAll(self,canvas,state):
		if (state[0] == "GET_NEIGHBORS"):
			candidate = state[1]
			neighbors = state[2]
			canvas.delete(ALL)
			self.drawAxis(canvas, self.cWidth, self.cHeight, self.sim.bounds)
			
			for p in self.points:
				if p == candidate:
					self.drawPoint(canvas, p, 2 * self.pRad, "yellow")
				elif p in neighbors:
					self.drawPoint(canvas, p, 2 * self.pRad, "orange")
				else:
					self.drawPoint(canvas, p, self.pRad)
                    
		elif (state[0] == "FIND_MEAN"):
			newMean = state[1]
			self.drawPoint(canvas, newMean, 2 * self.pRad, "green")
            
		elif (state[0] == "UPDATE_MEAN"):
			candidate = state[1]
			self.drawPoint(canvas, candidate, 2 * self.pRad, "red")
		else:
			canvas.delete(ALL)
			
			self.drawAxis(canvas, self.cWidth, self.cHeight, self.sim.bounds)
			centers = state[1]
			assignment = state[2]
			r = lambda: random.randint(0,255)
			colors = ['#%02X%02X%02X' % (r(),r(),r()) for i in xrange(len(centers))]
			for j in xrange(len(centers)):
				self.drawPoint(canvas, centers[j], 4 * self.pRad, colors[j])
				
			for i in xrange(len(self.points)):
				self.drawPoint(canvas, self.points[i], 2 * self.pRad, colors[assignment[i]])
		
G = MeanShiftGUI(False, 400, 400)
G.run()