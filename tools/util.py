import random

class Usage(Exception):
	
	def __init__(self, msg):
		self.msg = msg

def randomPoints(xRange, yRange, numPoints, clusters = 5):
    centers = [(random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])) for i in xrange(clusters)]
    points = []
    for i in xrange(numPoints):
        px = random.randint(xRange[0], xRange[1])
        py = random.randint(yRange[0], yRange[1])
        center = centers[random.randint(0,clusters - 1)]
        ratio = (1*random.random()/10) + .9

        if (center[0] >= px):
            px = px + int(ratio * abs(center[0] - px))
        else:
            px = px - int(ratio * abs(center[0] - px))

        if (center[1] >= py):
            py = py + int(ratio * abs(center[1] - py))
        else:
            py = py - int(ratio * abs(center[1] - py))

        points.append(Point(px, py))
    return (points, map(lambda c: Point(c[0], c[1]), centers))


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and (self.x == other.x and self.y == other.y))

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Rect(object):
        
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br

    def inBounds(self, point):
        return ((point.x >= self.tl.x) and
                (point.x <= self.br.x) and
                (point.y <= self.tl.y) and
                (point.y >= self.br.y))

    def __and__(self, other):
        print("Hello")
        if (self.tl.x > other.br.x or self.br.x < other.tl.x):
            return None
        if (self.tl.y < other.br.y or self.br.y > other.tl.y):
            return None
        c_l = max(self.tl.x, other.tl.x)
        c_r = min(self.br.x, other.br.x)
        c_t = min(self.tl.y, other.tl.y)
        c_b = max(self.br.y, other.br.y)
        return Rect(Point(c_l, c_t), Point(c_r, c_b))

    def __or__(self, other):
        c_l = min(self.tl.x, other.tl.x)
        c_r = max(self.br.x, other.br.x)
        c_t = max(self.tl.y, other.tl.y)
        c_b = min(self.br.y, other.br.y)
        return Rect(Point(c_l, c_t), Point(c_r, c_b))
        
    def size(self):
        return abs(self.br.x - self.tl.x, self.br.y - self.tl.y)
    
    def height(self):
        return abs(self.br.y - self.tl.y)
        
    def width(self):
        return abs(self.br.x - self.tl.x)
    
    def area(self):
        return abs((self.br.x - self.tl.x) * (self.br.y - self.tl.y))
    
    def __str__(self):
        return "<" + str(self.tl) + "," + str(self.br) + ">"