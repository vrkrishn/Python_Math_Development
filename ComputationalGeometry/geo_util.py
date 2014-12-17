import math

import sys
sys.path.append("../tools")

from gui_util import *
from util import *

def isLeft(L, C):
	return ((L.q.x - L.p.x) * (C.y - L.p.y) - (C.x - L.p.x) * (L.q.y - L.p.y))

def distance(p,q):
	return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)

def make_comparator(base):
	def compare(pA, pB):
		l = Line(base, pA)
		res = isLeft(l,pB)
		if (res > 0):
			return 1
		elif (res < 0):
			return -1
		else:
			if (distance(pA, base) > distance(pB, base)):
				return 1
			else:
				return -1
	return compare

def graham_scan(P):
	if (len(P) <= 3):
		return P
		
	#Select point in convex hull
	ind = 0
	y_min = P[0].y
	for i in xrange(1,len(P)):
		if (P[i].y < y_min):
			y_min = P[i].y
			ind = i
	
	base = P[ind]
	del P[ind]
	
	#sort points by angle
	compare = make_comparator(base)
	intermediate = sorted(P, cmp = compare)
	
	#build up convex hull
	hull = []
	last = base
	considering = intermediate[0]
	for i in xrange(1,len(intermediate)):
		possible = intermediate[i]
		res = isLeft(Line(last, possible), considering)
		if (res <= 0):
			considering = possible
		else:
			hull += [last]
			last = considering
			considering = possible
	hull += [considering]
	return hull
	
def convex_hull(P):
	return graham_scan(P)
	
p_list = randomPoints((0,100), (0, 100), 20, -1)
print map(lambda s: str(s), convex_hull(p_list))

print isLeft(Line(Point(0,0), Point(100,0)), Point(5, 0))


class Sim(Simulation):
	
	def __init__(self, xMin, xMax, yMin, yMax, inputPoints = None):
		super(Sim, self).__init__(xMin, xMax, yMin, yMax)
		
		P = inputPoints
		if (P == None):
			P = randomPoints((0,100), (0, 100), 20, -1)
		self.P = P
		
	def step(self):
		hull = convex_hull(P)
		return ['FINISHED', convex_hull, self.P]

class SimGUI(GUI):
	
	def __init__(self, canvasWidth, canvasHeight):
		
		xMin = 0
		xMax = 100
		yMin = 0
		yMax = 100
		
		game = Sim(xMin, xMax, yMin, yMax)
		super(SimGUI, self).__init__(False, canvasWidth, canvasHeight, game, 10)

	def redrawAll(self, canvas, state):
		gui_points = map(lambda p: self.CT.MtoV(p), state[2])
		gui_hull = map(lambda p: self.CT.MtoV(p), state[1])
		
		self.drawAxis(canvas, self.cWidth, self.cHeight, self.sim.bounds)
		for p in gui_points:
			self.drawPoint(canvas, p, 1)
			
		for i in xrange(1,len(gui_hull)):
			canvas.create_line(gui_hull[i-1].x, gui_hull[i-1].y , gui_hull[i].x, gui_hull[i].y, fill="red")
		canvas.create_line(gui_hull[0].x, gui_hull[0].y , gui_hull[-1].x, gui_hull[-1].y, fill="red")
		
S = SimGUI(400, 400)
S.run()
	
	