import math

import sys
sys.path.append("../tools")

from gui_util import *
from util import *

#----------------------------------------------------------------------#
#--------------------      Geometry Utils       -----------------------#
#----------------------------------------------------------------------#

def isLeft(L, C):
	return ((L.q.x - L.p.x) * (C.y - L.p.y) - (C.x - L.p.x) * (L.q.y - L.p.y))

def distance(p,q):
	return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)

def triangle_area(a,b,c):
	return abs((a.x*(b.y-c.y) + b.x*(c.y - a.y) + c.x*(a.y - b.y))/2.0)

#----------------------------------------------------------------------#
#--------------------        Convex Hull        -----------------------#
#----------------------------------------------------------------------#

#graham_scan: uses the graham scan approach to find the convex hull around
#			  a set of points
# @params: P - the set of points in a 2-D plane
# @return: the convex hull of a set of points
def graham_scan(P_inp):
	P = map(lambda p: p, P_inp)
	if (len(P) <= 2):
		return P, len(P)
	
	if (len(P) == 3):
		if (isLeft(Line(P[0], P[1]), P[2]) < 0):
			P[2], P[1] = P[1], P[2]
		return (P, 3)
		
	def make_comparator(base):
		def compare(pA, pB):
			l = Line(base, pA)
			res = isLeft(l,pB)
			if (res > 0):
				return -1
			elif (res < 0):
				return 1
			else:
				if (distance(pA, base) > distance(pB, base)):
					return 1
				else:
					return -1
		return compare
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
	hull = [intermediate[len(intermediate) - 1]] + [base] + intermediate
	hp = 1
	for i in xrange(2, len(hull)):
		while(isLeft(Line(hull[hp-1], hull[hp]), hull[i]) <= 0):
			if (hp > 1):
				hp -= 1
			elif (i == len(hull)):
				break
			else:
				i += 1
		hp += 1
		hull[hp], hull[i] = hull[i], hull[hp]
	
	return (hull, hp)
	
def convex_hull(P):
	return graham_scan(P)

#----------------------------------------------------------------------#
#-----------------           Closest Pairs          -------------------#
#----------------------------------------------------------------------#

def closest_pair_naive(P):
	d, d_pair = None, None
	for i in xrange(len(P)):
		root = P[i]
		for j in xrange(len(P)):
			if (j == i):
				continue
			check = P[j]
			if (d == None or distance(root, check) < d):
				d = distance(root, check)
				d_pair = (root, check)
	return d, d_pair

def closest_pair_dnc(P):
	def _closest_pair_dnc(Px, Py):
		if (len(Px) < 2):
			return (None, None)
		elif len(Px) == 2:
			return (distance(Px[0], Px[1]), (Px[0], Px[1]))
		else:
			n = len(Px)
			xmid = Px[n/2]
			
			yL = Builtin.filter(lambda p: p.x < xmid.x, Py)
			yR = Builtin.filter(lambda p: p.x >= xmid.x, Py)
			
			if (len(yL) < (n/2)):
				extra = len(yR) - n + n/2
				yL = yL + yR[0: extra]
				yR = yR[extra:]
				
			if (len(yR) < n - n/2):
				extra = len(yL) - n/2
				yR = yL[len(yL) - extra:] + yR
				yL = yL[0: len(yL) - extra]
			
			
			ld, l_pair = _closest_pair_dnc(Px[0:n/2], yL)
			rd, r_pair = _closest_pair_dnc(Px[n/2:], yR)
			
			d, d_pair = ld, l_pair
			if (ld == None or (rd != None and ld != None and rd < ld)):
				d, d_pair = rd, r_pair
		
			ySet = filter(lambda i: abs(Py[i].x - xmid.x) <= d, range(n))
			for i in ySet:
				base_p = Py[i]
				ptr = i+1
				#Check Up
				while (ptr < n and abs(Py[ptr].y - base_p.y) < d):
					cur_d = distance(Py[ptr], base_p)
					if (cur_d < d):
						d, d_pair = (cur_d, (base_p, Py[ptr]))
					ptr += 1
				
				#Check down
				ptr = i-1
				while (ptr >= 0 and abs(Py[ptr].y - base_p.y) <= d):
					cur_d = distance(Py[ptr], base_p)
					if (cur_d < d):
						d, d_pair = (cur_d, (base_p, Py[ptr]))
					ptr -= 1
			
			return (d, d_pair)
			
	Py = sorted(P, key=lambda p: p.y)
	Px = sorted(P, key=lambda p: p.x)
	
	return _closest_pair_dnc(Px, Py)
				

def closest_pair(P):
	return closest_pair_dnc(P)

#----------------------------------------------------------------------#
#-----------------     Convex Hull Applications     -------------------#
#----------------------------------------------------------------------#
def left_path(P):
	temp = P
	hull = []
	last = None
	while (len(temp) > 1):
		cur = convex_hull(temp)
		c_hull = cur[0]
		hp = cur[1]
		if (last != None):
			ind = c_hull.index(last)
			print last
			print map(lambda s: str(s), c_hull)
			print ind
		hull += c_hull[0:hp]
		temp = c_hull[hp+1:]
		if (len(temp) != 0):
			last = c_hull[hp+1]
	return hull
		
def largest_triangle_hull(P):
	if (len(P) <= 2):
		return None
		
	data,hp = convex_hull(P)
	hull = data[0:hp+1]
	A_f,B_f,C_f = -1, -1, -1
	max_area = 0
	finished = False
	for A in xrange(len(hull)):
		finished = False
		B,C = (A+1) % len(hull), (A+2) % len(hull)
		
		while (not finished):
			if (triangle_area(hull[A], hull[B], hull[C]) < 
				triangle_area(hull[A], hull[B], hull[(C+1)% len(hull)])):
				C = (C+1) % len(hull)
				continue
		
			if (triangle_area(hull[A], hull[B], hull[C]) < 
				triangle_area(hull[A], hull[(B+1) % len(hull)], hull[C])):
				B = (B+1) % len(hull)
				continue
			
			finished = True
			
		cur_area = triangle_area(hull[A], hull[B], hull[C])
		if (cur_area > max_area):
			max_area = cur_area
			A_f, B_f, C_f = A,B,C
			
	return (hull[A_f], hull[B_f], hull[C_f])
	
def largest_triangle(P):
	return largest_triangle_hull(P)


class Sim(Simulation):
	
	def __init__(self, xMin, xMax, yMin, yMax, inputPoints = None):
		super(Sim, self).__init__(xMin, xMax, yMin, yMax)
		
		P = inputPoints
		if (P == None): 
			P = randomPoints((xMin,xMax), (yMin, yMax), 35, -1)
		self.P = P
		
	def step(self):
		hull,hp = convex_hull(self.P)
		print "Computed Convex Hull"
		
		tri = largest_triangle(self.P)
		print "Computed Largest Triangle"
		
		(c_dist, pair) = closest_pair(self.P)
		print "Computed Closest Pair"
		return ['FINISHED', hull[0:hp], tri, pair, self.P]

class SimGUI(GUI):
	
	def __init__(self, canvasWidth, canvasHeight):
		
		xMin = -10
		xMax = 50
		yMin = -10
		yMax = 50
		
		game = Sim(xMin, xMax, yMin, yMax)
		super(SimGUI, self).__init__(False, canvasWidth, canvasHeight, game, 10)

	def redrawAll(self, canvas, state):
		gui_hull = map(lambda p: self.CT.MtoV(p), state[1])
		gui_tri = map(lambda p: self.CT.MtoV(p), state[2])
		
		self.drawAxis(canvas, self.cWidth, self.cHeight, self.sim.bounds)
		for p in state[len(state) - 1]:
			self.drawPoint(canvas, p, 2, "black")
						   
		for i in xrange(1,len(gui_hull)):
			canvas.create_line(gui_hull[i-1].x, gui_hull[i-1].y , 
						   	   gui_hull[i].x, gui_hull[i].y, fill="green")
		canvas.create_line(gui_hull[0].x, gui_hull[0].y , 
						   gui_hull[-1].x, gui_hull[-1].y, fill="green")
						   
		for i in xrange(1,len(gui_tri)):
			canvas.create_line(gui_tri[i-1].x, gui_tri[i-1].y , 
						   	   gui_tri[i].x, gui_tri[i].y, fill="red")
		canvas.create_line(gui_tri[0].x, gui_tri[0].y , 
						   gui_tri[-1].x, gui_tri[-1].y, fill="red")
						   
		for p in state[3]:
			self.drawPoint(canvas, p, 3, "blue")

def test(ITERATIONS):
	print "------------------------------\nTesting Closest Pair"
	for i in xrange(ITERATIONS):
		P = randomPoints((0,100), (0, 100), random.randint(7,50), -1)
		(c_dist, c_pair) = closest_pair(P)
		(n_dist, n_pair) = closest_pair_naive(P)
		
		if (not abs(n_dist - c_dist) < .00001):
			print "Error on iteration: %d" %(i)
			print "Naive: %f, (%s, %s)" %(n_dist, str(n_pair[0]), str(n_pair[1]))
			print "DNC: %f, (%s, %s)" %(c_dist, str(c_pair[0]), str(c_pair[1]))
	print "Finished Testing Closest Pair"


#test(1000)
S = SimGUI(800, 800)
S.run()