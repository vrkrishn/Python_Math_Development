from trees import *

#-----------------------------------------------------------#
#----------------    Interval Trees    ---------------------#
#-----------------------------------------------------------#

# A pythonic implementation of interval trees

#-------------------   Headers   ---------------------------#

# create_trees(keys): Create a new interval tree object from keys
# @params: each of the endpoints of every segment in the key search
#		   that is sorted in increasing order
# @return: Interval Tree object
# @cost: O(n)

# update(T, lo, high, dif): Update the interval by adding a certain dif
#						    to any range of the data
# @params: T - interval trees
#		   lo/hi - the bounds of the interval used to update the tree
#		   dif - value to be added to each of the intervals in question
# @return: None (Updates T)
# @cost: O(log(n))

# push_through(T): Flush all lazy updates through the tree
# @params: T - interval tree
# @return: None (Updates T)
# @cost: O(nlog(n))

# find_max(T): Find the maximum leaf value in the tree
# @params: T - interval tree
# @return: maximum value element in T
# @cost: O(n)

#--------------------   Structs    ----------------------------#
class Leaf(object):
	
	def __init__(self, x):
		self.left = None
		self.right = None
		self.x = x
		self.C_max = 0
		self.C = 0
		
	def __str__(self):
		return "Leaf(%s -> %d, %d)" % (str(self.x), self.C, self.C_max)
		
class Node(object):
	
	def __init__(self, x):
		self.left = None
		self.right = None
		self.x = x
		self.L_max = 0
		self.L = 0
		self.R_max = 0
		self.R = 0
		
	def __str__(self):
		return "Node(%s -> %d, %d, %d, %d)" % (str(self.x), self.L, self.L_max, self.R, self.R_max)

#--------------------   Code    ----------------------------#
class IntervalTree(object):
	
	@staticmethod
	def create_tree(keys):
		leafs = []
		for i in xrange(len(keys) - 1):
			leaf = Leaf((keys[i], keys[i+1]))
			leafs += [leaf]
		last = Leaf((keys[len(keys) - 1], keys[len(keys) - 1] + 1))
		leafs += [last]
		
		root = leafs
		while len(root) > 1:
			new_roots = []
			for i in xrange(len(root)/2):
				l_pair = root[2*i]
				r_pair = root[2*i + 1]
				n = Node((l_pair.x[0],r_pair.x[1]))
				n.left = l_pair
				n.right = r_pair
				new_roots += [n]
			
			if (len(root) % 2 == 1):
				r_pair = root[len(root) - 1]
				l_pair = new_roots[len(new_roots) - 1]
				n = Node((l_pair.x[0],r_pair.x[1]))
				n.left = l_pair
				n.right = r_pair
				new_roots += [n]
				new_roots.remove(l_pair)
			root = new_roots
		
		root = root[0]
		
		T = TreeHeader("Interval Tree", len(leafs))
		T.last = last
		T.root = root
		T.leaves = leafs
		return T
		
	@staticmethod
	def str(T):
		def _tree_str(cur, offset):
			if (cur == None):
				return "\n" + offset + "None"
			
			result = "\n" + offset + "%s" %(str(cur))
			result += offset + _tree_str(cur.left, offset + "    ")
			result += offset + _tree_str(cur.right, offset + "    ")
			return result
		
		result = "\n" + T.name
		result += "\nSize: %d\n" %(T.size)
		if (T.root != None):
			result += _tree_str(T.root, "")
		return result
	
	@staticmethod
	def update(T, lo, high, isTop):
		if (T.root != None):
			IntervalTree.findBoth(T.root, lo, high, 0, 0, isTop)
	
	@staticmethod
	def get_max(T):
		def _get_max(cur):
			if IntervalTree.isLeaf(cur):
				return cur.C_max
			else:
				return max(_get_max(cur.left), _get_max(cur.right))
		
		if (T.root == None):
			return 0
				
		return _get_max(T.root)
			
	@staticmethod
	def push_through(T):
		for i in xrange(len(T.leaves) - 1):
			leaf = T.leaves[i]
			IntervalTree.update(T, leaf.x[0], leaf.x[1], 0)
		IntervalTree.update(T, T.last.x[0], T.last.x[0], 0)
			
	@staticmethod
	def isLeaf(node):
		return (node.left == None and node.right == None)
	
	@staticmethod
	def less(cur, lo, hi):
		if IntervalTree.isLeaf(cur.left):
			return False
		
		l_interval = cur.left.x
		return (l_interval[0] <= lo and l_interval[1] > hi)
	
	@staticmethod
	def greater(cur, lo, hi):
		if IntervalTree.isLeaf(cur.right):
			return False
		
		r_interval = cur.right.x
		return (r_interval[0] <= lo and (r_interval[1] > hi))
	
	@staticmethod
	def internal(cur, lo, hi):
		if (IntervalTree.isLeaf(cur.left) or IntervalTree.isLeaf(cur.right)):
			return True
		
		l_interval = cur.left.x
		r_interval = cur.right.x
		return (l_interval[0] <= lo and l_interval[1] > lo and 
						r_interval[0] <= hi and (r_interval[1] > hi))
	
	@staticmethod
 	def findBoth(cur, lo, hi, up, up_max, isTop):
		cur.L_max = max(cur.L_max, cur.L + up_max)
		cur.L = cur.L + up
	
		cur.R_max = max(cur.R_max, cur.R + up_max)
		cur.R = cur.R + up
		
		if (IntervalTree.less(cur, lo, hi)):
			IntervalTree.findBoth(cur.left, lo, hi, cur.L, cur.L_max, isTop)
			cur.L = 0
			cur.L_max = 0
			
		elif (IntervalTree.greater(cur, lo, hi)):
			IntervalTree.findBoth(cur.right, lo, hi, cur.R, cur.R_max, isTop)
			cur.R = 0
			cur.R_max = 0
			
		elif (IntervalTree.internal(cur, lo, hi)):
			IntervalTree.findLeft(cur.left, lo, cur.L, cur.L_max, isTop)
			IntervalTree.findRight(cur.right, hi, cur.R, cur.R_max,  isTop)
			cur.L = 0
			cur.L_max = 0
			cur.R = 0
			cur.R_max = 0
			
		else:
			print "Error"
			print cur, lo, hi
			
	@staticmethod
	def findLeft(cur, lo, up, up_max, isTop):
		if (lo <= cur.x[0] and not IntervalTree.isLeaf(cur)):
			cur.R_max = max(cur.R_max, cur.R + up_max, cur.R + up + isTop)
			cur.R = cur.R + up + isTop
			IntervalTree.findLeft(cur.left, lo, cur.L + up, max(cur.L_max, cur.L + up_max), isTop)
			cur.L = 0
			cur.L_max = 0
		
		elif (lo > cur.x[0] and not IntervalTree.isLeaf(cur)):
			cur.L_max = max(cur.L_max, cur.L + up_max, cur.L + up + isTop)
			cur.L = cur.L + up
			IntervalTree.findLeft(cur.right, lo, cur.R + up, max(cur.R_max, cur.R + up_max), isTop)
			cur.R = 0
			cur.R_max = 0
		
		elif (cur.x[0] == lo and IntervalTree.isLeaf(cur)):
			cur.C_max = max(cur.C_max, (cur.C + up_max), cur.C + up + isTop)
			cur.C = cur.C + up + isTop
	
	@staticmethod
	def findRight(cur, hi, up, up_max, isTop):
		if (hi > cur.x[0] and not IntervalTree.isLeaf(cur)):
			cur.L_max = max(cur.L_max, cur.L + up_max, cur.L + up + isTop)
			cur.L = cur.L + up + isTop
			IntervalTree.findRight(cur.right, hi, cur.R + up, max(cur.R_max, cur.R + up_max), isTop)
			cur.R = 0
			cur.R_max = 0
		
		elif (hi <= cur.x[0] and not IntervalTree.isLeaf(cur)):
			cur.R_max = max(cur.R_max, cur.R + up_max, cur.R + up + isTop)
			cur.R = cur.R + up
			IntervalTree.findRight(cur.left, hi, cur.L + up, max(cur.L_max, cur.L + up_max), isTop)
			cur.L = 0
			cur.L_max = 0
		
		elif (cur.x[0] == hi and IntervalTree.isLeaf(cur)):
			cur.C_max = max(cur.C_max, (cur.C + up_max), cur.C + up + isTop)
			cur.C = cur.C + up + isTop
			
		
def main():
	for ITER in xrange(5):
		T = IntervalTree.create_tree(range(6))
		for i in xrange(5):
			i = random.randint(0,5)
			j = random.randint(0,5)
			IntervalTree.update(T, min(i,j), max(i,j), 1)
		print IntervalTree.str(T)
		IntervalTree.push_through(T)
		print IntervalTree.get_max(T)
			
if __name__ == "__main__":
	main()