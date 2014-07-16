from sympy import *
init_printing(use_unicode=True)

import random

def print_array(a):
	print reduce(lambda a,b: a+ " "+b, map(lambda e: str(e), a))
	
def equals_array(f):
	def g(A,B):
		n = len(A)
		m = len(B)
		if n != m:
			return False
			
		return reduce(lambda a,b: a and b, map(lambda i: f(A[i], B[i]), range(n)))
	return g

class Point:
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"
		
class Value:
	
	def __init__(self,x, error = False):
		self.x = x
		self.error = error
		
	def get(self):
		if self.error:
			return None
		else:
			return self.x
			
	def __str__(self):
		if self.error:
			return "NONE"
		else:
			return "SOME(" + str(self.x) +")"
		
class Encoder:
	
	def encode(self, message, error):
		n = len(message)
		num_points = n + error
		
		def f(x):			
			inter = map(lambda i: x**(i) * message[i], range(n))
			return reduce(lambda a,b: a+b, inter)
			
		return [Value(f(i)) for i in xrange(num_points)]
		
class Decoder:
	
	def decode(self, message, precision = 0):

		indexed = map(lambda i: Point(i, message[i].get()), range(len(message)))
		filtered = filter(lambda p: p.y != None, indexed)
		
		def LagrangeInterpolation(pointList):
			x = symbols("x")

			def LagrangeBasisPolynomialFactory(xList, j):
				terms = [(x - xList[i])/(xList[j] - xList[i]) if i != j else 1 for i in xrange(len(xList))]
				return reduce(lambda a,b: a * b, terms, 1)

			if (len(filtered) == 0):
				print "[ERROR]: Message cannot be extrapolated from available data points"
				return [0.0]

			xList = [pointList[i].x for i in xrange(len(pointList))]
			basis = map(lambda i: pointList[i].y * LagrangeBasisPolynomialFactory(xList,i), range(len(pointList)))
			result = Poly(simplify(expand(reduce(lambda a,b: a+b, basis, 0))),x).all_coeffs()
			
			#Todo check correctness of result
			
			return result
			
		return LagrangeInterpolation(filtered)[::-1]
	
class NoiseEmulator:
	
	def emulateNoise(self,message,error):
		
		def random_subset(iterator, K):
		    result = []
		    N = 0

		    for item in iterator:
		        N += 1
		        if len( result ) < K:
		            result.append( item )
		        else:
		            s = int(random.random() * N)
		            if s < K:
		                result[s] = item

		    return result
		
		subset = random_subset(message, random.randint(0,error))
		for item in subset:
			item.error = True
			
		return message	


e = Encoder()
d = Decoder()
N = NoiseEmulator()
partial = e.encode([0,0,1],9)
noisy = N.emulateNoise(partial,9)
print d.decode(noisy, 10)


				
			
