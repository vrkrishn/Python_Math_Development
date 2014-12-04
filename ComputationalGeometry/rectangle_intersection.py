import random

import sys
sys.path.append('../tools')

from gui_util import *
from util import *
from interval_tree import *


class RectangleSimulation(Simulation):
	
	def __init__(self, xMin, xMax, yMin, yMax, inputRect = None):
		super(RectangleSimulation, self).__init__(xMin, xMax, yMin, yMax)
	
		S = inputRect
		if (inputRect == None):
			S = self.randomRectangles((xMin, xMax), (yMin, yMax), 50)
			
		self.S = S
	
	def step(self):
		maximum = self.rectangle_intersection(self.S)
		return ["FINISHED", maximum, self.S]
	
	def rectangle_intersection(self, S):
		keys = map(lambda r: r.tl.x, S) + map(lambda r: r.br.x, S)
		keys = sorted(keys)
		T = IntervalTree.create_tree(keys)
	
		events = map(lambda r: (r.tl.y, (r.tl.x, r.br.x) , -1), S) + map(lambda r: (r.br.y, (r.tl.x, r.br.x), 1), S)
		events = sorted(events, key = lambda ev: ev[0])
	
		print map(lambda r: str(r), S)
	
		for i in xrange(len(events)):
			ev = events[i]
			#print 
			#print "Inserting ", ev
			IntervalTree.update(T, ev[1][0], ev[1][1], ev[2])
			#print IntervalTree.str(T)
		
		IntervalTree.push_through(T)
		return IntervalTree.get_max(T)
		
	def randomRectangles(self, xRange, yRange, n):
	
		x_vals = random.sample(range(xRange[0], xRange[1]), 2*n)
		y_vals = random.sample(range(yRange[0], yRange[1]), 2*n)
	
		pairs = zip(x_vals, y_vals)
	
		rects = []
		for i in xrange(len(pairs)/2):
			tl = Point(min(pairs[2*i][0], pairs[2*i+1][0]), max(pairs[2*i][1], pairs[2*i+1][1]))
			br = Point(max(pairs[2*i][0], pairs[2*i+1][0]), min(pairs[2*i][1], pairs[2*i+1][1]))
			rects += [Rect(tl, br)]

		return rects
	

class RectangleIntersectionGUI(GUI):
	
	def __init__(self, canvasWidth, canvasHeight):
		
		xMin = 0
		xMax = 100
		yMin = 0
		yMax = 100
		
		game = RectangleSimulation(xMin, xMax, yMin, yMax)
		super(RectangleIntersectionGUI, self).__init__(False, canvasWidth, canvasHeight, game, 10)

	def redrawAll(self, canvas, state):
		print "---------------------------"
		print "Max Intersection: ", state[1]
		rects = state[2]
		gui_rects = map(lambda r: Rect(self.CT.MtoV(r.tl), self.CT.MtoV(r.br)), rects)
		
		colors = []
		red = 255;
		green = 0;
		stepSize = 2 * 255 / (state[1] + 1)
		while(green < 255):
			colors += ["#%02x%02x%02x" %(red, green, 0)] 
			green += stepSize 
			if(green > 255): 
				green = 255 
		
		while(red > 0): 
			red -= stepSize 
			if(red < 0): 
				red = 0
			colors += ["#%02x%02x%02x" %(red, green, 0)]

		
		for row in xrange(self.cWidth):
			for col in xrange(self.cHeight):
				intersection = 0
				
				for r in gui_rects:
					if (row > r.tl.x and row < r.br.x and
						col > r.tl.y and col < r.br.y):
						intersection += 1
					
				canvas.create_rectangle(row, col, row + 1, col + 1, fill = colors[intersection], width = 0)
					
		self.drawAxis(canvas, self.cWidth, self.cHeight, self.sim.bounds)
		for r in gui_rects:
			canvas.create_rectangle(r.tl.x, r.tl.y, r.br.x, r.br.y, width = 1)
		
		
		print gui_rects

def inputRectangles(points):
	S = []
	for p in points:
		r = Rect(Point(p[0][0], p[0][1]), Point(p[1][0], p[1][1]))
		S += [r]
	return S
	
def main():
	T = RectangleIntersectionGUI(400, 400)
	T.run()
	
if __name__ == "__main__":
	main()
