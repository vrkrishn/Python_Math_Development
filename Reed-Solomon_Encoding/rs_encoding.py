from sympy import *
init_printing(use_unicode=True)

import sys
import argparse

sys.path.append('../tools')
from util import Usage

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
	
class Value:
	
	def __init__(self,x, error = False):
		self.x = x
		self.error = error
		
	def get(self):
		if (random.random() > error):
			return x
		else:
			return None
		
class Encoder:
	
	def encode_str(self, message, error):
		msg = message.split(" ")
		msg = [map(lambda c: ord(c), m) for m in msg]
		encoded = [self.encode(m,error) for m in msg]
		
		return encoded
	
	def encode(self, message, error):
		n = len(message)
		num_points = int(n * (1 + error)) + 1
		
		def f(x):			
			inter = map(lambda i: x**(i) * message[i], range(n))
			return reduce(lambda a,b: a+b, inter)
			
		return [f(i) for i in xrange(num_points)]
		
class Decoder:
	
	def decode_str(self, message):
		words = [self.decode(m) for m in message]
		print words
		message = map(lambda a: ''.join(map(lambda c: chr(c), a)), words)
		return ' '.join(message)
	
	def decode(self, message):
		indexed = map(lambda i: Point(i, message[i]), range(len(message)))
		filtered = filter(lambda p: p.y != None, indexed)
		
		def LagrangeInterpolation(pointList):
			x = symbols("x")

			def LagrangeBasisPolynomialFactory(xList, j):
				terms = [(x - xList[i])/(xList[j] - xList[i]) if i != j else 1 for i in xrange(len(xList))]
				return reduce(lambda a,b: a * b, terms, 1)

			if (len(filtered) == 0):
				print "[ERROR]: Message cannot be extrapolated from available data points"
				return None

			xList = [pointList[i].x for i in xrange(len(pointList))]
			basis = map(lambda i: pointList[i].y * LagrangeBasisPolynomialFactory(xList,i), range(len(pointList)))
			result = Poly(simplify(expand(reduce(lambda a,b: a+b, basis, 0))),x).all_coeffs()
			
			#Todo check correctness of result
			return result
			
		return LagrangeInterpolation(filtered)[::-1]
	
class NoiseEmulator:
	
	def emulateNoise(self,message,error):
		
		msg = []
		
		for word in message:
			temp = []
			for i in word:
				if random.random() > error:
					temp += [i]
				else:
					temp += [ None ]
			msg += [temp]
		return msg	


def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--test', help = 'run the module test', action = 'store_true')
	parser.add_argument('--error')
	args = parser.parse_args()
	
	if (args.test):
		e = Encoder()
		d = Decoder()
		N = NoiseEmulator()
		error = 0.1
		
		print "-------------------------------------"
		print "Running Test of Reed Solomon Encoding"
		print "Input:  This is a test of the Reed Solomon encoding mechanism."
		print "-------------------------------------"
		print "Encoding String for %d percent error rate" %(error * 100)
		partial = e.encode_str('This is a test of the Reed Solomon encoding mechanism.', error)
		print "Encoded: ", partial
		print "-------------------------------------"
		print "Emulating Noise"
		noisy = N.emulateNoise(partial, error)
		print "Lossy String: ", noisy
		print "-------------------------------------"
		print "Decoding Message"
		decoded = d.decode_str(noisy)
		print "Output:  ",decoded 
		print "-------------------------------------"
	
if __name__ == "__main__":
    sys.exit(main())

				
			
