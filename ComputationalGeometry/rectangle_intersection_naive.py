import random
import itertools

def max_overlap_naive(S, xRange, yRange):
	def count_intersections(point, S):
		return sum(map(lambda r: r.exists_point(point), S))
	
	coords = itertools.product(range(xRange[0], xRange[1]), range(yRange[0], yRange[1]))
	points = map(lambda t: Point(t[0], t[1]), coords) 
	out = map(lambda p: count_intersections(p, S), points)
	return (max(out), points[out.index(max(out))])

class Point(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

class Rect:
	
	def __init__(self,tl, br):
		self.tl = tl
		self.br = br
		
	def __str__(self):
		return "[" + str(self.tl) + ", " + str(self.br) + "]"
	
	def exists_point(self, point):
		return (self.tl.x < point.x and self.br.x > point.x and
				self.br.y < point.y and self.tl.y > point.y)
				
	def height(self):
		return self.tl.y - self.br.y
		
	def width(self):
		return self.br.x - self.tl.x

def test():
	S = randomRectangles(xRange, yRange, 10)
	result = max_overlap_naive(S, xRange, yRange)
	result2 = max_overlap_better(S, xRange, yRange)
	
test()