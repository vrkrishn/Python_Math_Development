class BSTNode(object):
	
	def __init__(self, key):
		self.x = key
		self.left = None
		self.right = None
		
class Leaf(BSTNode):
	
	def __init__(self, x):
		super(Leaf, self).__init__(x)
		self.C_max = 0
		self.C = 0
		
class Node(BSTNode):
	
	def __init__(self, x):
		super(Node, self).__init__(x)
		self.L_max = 0
		self.L = 0
		self.R_max = 0
		self.R = 0
	
class IntervalTree(object):

  @staticmethod
	def createIntervalTree(S):
		x_ints = map(lambda r: r.tl.x, S) + map(lambda r: r.br.x, S)
		x_ints = sorted(x_ints)
	
	@staticmethod
	def update(T, lo, high, isTop):
		if (T.root != None):
			IntervalTree.findBoth(T.root, lo, high, 0, 0, isTop)
	
  @staticmethod
	def isLeaf(node):
		return (node.left == None and node.right == None)
	
	@staticmethod
 	def findBoth(cur, lo, hi, up, up_max, isTop):
		cur.L_max = max(cur.L_max, cur.L + up_max)
		cur.L = cur.L + up
	
		cur.R_max = max(cur.R_max, cur.R + up_max)
		cur.R = cur.R + up
		
		if (cur.x >= hi):
			IntervalTree.findBoth(cur.left, lo, hi, cur.L, cur.L_max, isTop)
			cur.L = 0
			cur.L_max = 0
			
		elif (cur.x < lo):
			IntervalTree.findBoth(cur.right, lo, hi, cur.R, cur.R_max, isTop)
			cur.R = 0
			cur.R_max = 0
			
		else:
			IntervalTree.findLeft(cur.left, lo, cur.L, cur.L_max, isTop)
			IntervalTree.findRight(cur.right, hi, cur.R, cur.R_max,  isTop)
			cur.L = 0
			cur.L_max = 0
			cur.R = 0
			cur.R_max = 0

  @staticmethod
	def findLeft(cur, lo, up, up_max, isTop):
		if (lo <= cur.x and not isLeaf(cur)):
			cur.R_max = max(cur.R_max, cur.R + up_max, cur.R + up + isTop)
			cur.R = cur.R + up + isTop
			IntervalTree.findLeft(cur.left, lo, cur.L + up, max(cur.L_max, cur.L + up_max), isTop)
			cur.L = 0
			cur.L_max = 0
		
		elif (cur.x < lo and not isLeaf(cur)):
			cur.L_max = max(cur.L_max, cur.L + up_max, cur.L + up + isTop)
			cur.L = cur.L + up
			IntervalTree.findLeft(cur.right, lo, cur.R + up, max(cur.R_max, cur.R + up_max), isTop)
			cur.R = 0
			cur.R_max = 0
		
		elif (cur.x == lo and isLeaf(cur)):
			cur.C_max = max(cur.C_max, (cur.C + up_max), cur.C + up + isTop)
			cur.C = cur.C + up + isTop

  @staticmethod
	def findRight(cur, hi, up, up_max, isTop):
		if (hi >= cur.x and not isLeaf(cur)):
			cur.L_max = max(cur.L_max, cur.L + up_max, cur.L + up + isTop)
			cur.L = cur.L + up + isTop
			IntervalTree.findRight(cur.right, hi, cur.R + up, max(cur.R_max, cur.R + up_max), isTop)
			cur.R = 0
			cur.R_max = 0
			
		elif (hi < cur.x and not isLeaf(cur)):
			cur.R_max = max(cur.L_max, cur.L + up_max, cur.L + up + isTop)
			cur.R = cur.L + up
			IntervalTree.findRight(cur.left, hi, cur.L + up, max(cur.L_max, cur.L + up_max), isTop)
			cur.L = 0
			cur.L_max = 0
			
		elif (cur.x == hi and isLeaf(cur)):	
			cur.C_max = max(cur.C_max, (cur.C + up_max), cur.C + up + isTop)
			cur.C = cur.C + up + isTop
		

		