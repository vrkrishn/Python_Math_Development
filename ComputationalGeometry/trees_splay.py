import random
from trees import *

class SplayNode:
	def __init__(self, key, data, base, update, parent = None):
		self.key = key;
		self.data = data
		self.parent = parent
		self.left = None
		self.right = None
		self.base = base
		self.update = lambda : update(self, self.left, self.right)
		
	def __str__(self):
		return ("Node(%s, %s, %d)" % (str(self.key), str(self.data), self.base))

class SplayHeader:
	
	def __init__(self, update, base):
		self.root = None
		self.update = update
		self.base = base

class BST(object):	
	@staticmethod
	def str(T):
		def _str(current, offset):
			result = offset + str(current)
			if (current != None):
				result += "\n" + _str(current.left, offset + "    ")
				result += "\n" + _str(current.right, offset + "    ")
			return result
		return _str(T.root, "")
	
	@staticmethod
	def create_tree(update, base):
		return BSTHeader(update, base)
	
	@staticmethod
	def is_ordered(T):
		def _is_ordered(current, b_min, b_max):
			if (current == None):
				return True
				
			result = True
			if (b_min != None):
				result &= current.key > b_min
			if (b_max != None):
				result &= current.key < b_max
			result &= _is_ordered(current.left, b_min, current.key)
			result &= _is_ordered(current.right, current.key, b_max)
			return result
			
		return _is_ordered(T.root, None, None)
	
	@staticmethod
	def is_correct(T):
		def _is_correct(current):
			if (current == None):
				return True
				
			v = current.base
			check = T.update(current.left, current.right)
			
			if (check != v):
				return False
				
			return (_is_sized(current.left) and _is_sized(current.right))
			
		return _is_correct(T.root)
	
	@staticmethod
	def is_valid_tree(T):
		assert(BST.is_ordered(T))
		assert(BST.is_sized(T))
		return True
		
	@staticmethod
	def find(T, key):
		def _find(current, key):
			if (key < current.key):
				if (current.left == None):
					return None
				else:
					return _find(current.left, key)
			elif (key > current.key):
				if (current.right == None):
					return None
				else:
					return _find(current.right, key)
			else:
				return current
				
		if (T.root == None):
			return None
		else:
			return _find(T.root, key)
			
	@staticmethod
	def insert(T, key, data):
		def _insert(current, key, data, parent):
			if (key < current.key):
				if (current.left == None):
					current.left = BSTNode(key, data, parent)
					current.left.parent = current
				else:
					_insert(current.left, key, data, current)
			elif (key > current.key):
				if (current.right == None):
					current.right = BSTNode(key, data, parent)
					current.right.parent = current
				else:
					_insert(current.right, key, data, current)
			else:
				current.key = key
				current.data = data

		if (T.root == None):
			T.root = BSTNode(key, data, None)
			T.root.update()
			return T
		else:
			_insert(T.root, key, data, None)
			T.root.update()
			return T
			
	@staticmethod
	def value(T):
		if (T.root == None):
			return T.base
		else:
			return T.root.base

######################################################################
#####################				AVL Tree						######################
######################################################################


######################################################################
####################				Splay Tree						####################
######################################################################

class SplayTree(BST):
	@staticmethod
	def find(T, key):
		def _find(current, key):
			if (key < current.key):
				if (current.left == None):
					SplayTree.splay(T, current)
					return None
				else:
					return _find(current.left, key)
			elif (key > current.key):
				if (current.right == None):
					SplayTree.splay(T, current)
					return None
				else:
					return _find(current.right, key)
			else:
				SplayTree.splay(T, current)
				return current
				
		if (T.root == None):
			return None
		else:
			result = _find(T.root, key)
			return result
	
	@staticmethod
	def join(T1, T2):
		if (T1.root == None):
			return T2
		if (T2.root == None):
			return T1
			
		cur = T1.root
		r_child = T2.root
		while (cur.right != None):
			cur = cur.right
		SplayTree.splay(T1,cur)
		T1.root.right = r_child
		r_child.parent = T1.root
		T = SplayTree.create_tree(T1.update, T1.base)
		T.root = T1.root
		T.root.base = T.root.update()
		T1 = None
		T2 = None
		return T
		
	@staticmethod
	def split(T, key):
		SplayTree.find(T, key)
		
		T1 = SplayTree.create_tree(T.update, T.base)
		T2 = SplayTree.create_tree(T.update, T.base)
		
		if (T.root.key > key):
			T1.root = T.root.left
			if T1.root != None:
				T1.root.parent = None
			T2.root = T.root
			T2.root.left = None
			
		elif (T.root.key <= key):
			T2.root = T.root.right
			if T2.root != None:
				T2.root.parent = None
			T1.root = T.root
			T1.root.right = None
	
		T = None
		if (T1.root):
			T1.root.base = T1.root.update()
		if (T2.root):
			T2.root.base = T2.root.update()
		return (T1, T2)
	
	@staticmethod
	def insert(T, key, data):
		if (T.root == None):
			root = BSTNode(key, data, T.base, T.update, None)
			T.root = root
			return T
			
		(Tl, Tr) = SplayTree.split(T, key)
		T = SplayTree.create_tree(T.update, T.base)
		if (Tl.root != None and Tl.root.key == key):
			T.root = Tl.root
			T.root.data = data
			T.root.right = Tr.root
			if Tr.root != None:
				Tr.root.parent = T.root
			return T
		else:
			root = BSTNode(key, data, T.base, T.update, None)
			T.root = root
			T.root.right = Tr.root
			T.root.left = Tl.root
			if Tr.root != None:
				Tr.root.parent = root
				
			if (Tl.root != None):
				Tl.root.parent = root
			T.root.base = T.root.update()
			return T
			
	@staticmethod
	def delete(T, key):
		if (T.root == None):
			return T
		
		if (SplayTree.find(T,key) != None):
			T1 = SplayTree.create_tree(T.update, T.base)
			T2 = SplayTree.create_tree(T.update, T.base)
			T1.root = T.root.left
			if (T1.root):
				T1.root.parent = None
			T2.root = T.root.right
			if (T2.root):
				T2.root.parent = None
			Tout = SplayTree.join(T1, T2)
			return Tout
		else:
			return T
	
	@staticmethod
	def getKeys(T):
		if T.root == None:
			return []
		else:
			return getKeys(T.root.left) + [T.root.key] + getKeys(T.root.right)
	
	@staticmethod
	def splay(T, x):
		parent = x.parent
		#If x is the root
		if (parent == None):
			T.root = x
			x.parent = None
			return
		#Zig step
		elif (parent.parent == None):
			if (parent.left == x):
				x.parent = parent.parent
				parent.left = x.right
				if (parent.left != None):
					parent.left.parent = parent
				parent.parent = x
				x.right = parent
				T.root = x
				#update size
				parent.base = parent.update()
				x.base = x.update()
				
			elif (parent.right == x):
				x.parent = parent.parent
				parent.right = x.left
				if (parent.right != None):
					parent.right.parent = parent
				parent.parent = x
				x.left = parent
				T.root = x
				#update size
				parent.base = parent.update()
				x.base = x.update()
		else:
			grandparent = parent.parent
			#Zig Zig step
			if (grandparent.left == parent and parent.left == x):
				
				grandparent.left = parent.right
				if (grandparent.left != None):
					grandparent.left.parent = grandparent
				parent.left = x.right
				if (parent.left != None):
					parent.left.parent = parent
				
				x.parent = grandparent.parent
				parent.parent = x
				grandparent.parent = parent
				
				parent.right = grandparent
				x.right = parent
				
				#update size
				grandparent.base = grandparent.update()
				parent.base = parent.update()
				x.base = x.update()
				
				#Splay Further
				if (x.parent != None):
					if x.parent.left == grandparent:
						x.parent.left = x
					else:
						x.parent.right = x
					SplayTree.splay(T,x)
				else:
					T.root = x
				
			elif (grandparent.right == parent and parent.right == x):
				grandparent.right = parent.left
				if (grandparent.right != None):
					grandparent.right.parent = grandparent
				parent.right = x.left
				if (parent.right != None):
					parent.right.parent = parent
				
				x.parent = grandparent.parent
				parent.parent = x
				grandparent.parent = parent
				
				parent.left = grandparent
				x.left = parent
				
				#update size
				grandparent.base = grandparent.update()
				parent.base = parent.update()
				x.base = x.update()
				
				#Splay Further
				if (x.parent != None):
					if x.parent.left == grandparent:
						x.parent.left = x
					else:
						x.parent.right = x
					SplayTree.splay(T,x)
				else:
					T.root = x
				
			#Zig Zag step
			elif (grandparent.left == parent and parent.right == x):
				grandparent.left = x.right
				if (grandparent.left != None):
					grandparent.left.parent = grandparent
				parent.right = x.left
				if (parent.right != None):
					parent.right.parent = parent
				
				x.parent = grandparent.parent
				parent.parent = x
				grandparent.parent = x
				
				x.right = grandparent
				x.left = parent
				
				#update size
				grandparent.base = grandparent.update()
				parent.base = parent.update()
				x.base = x.update()
				
				#Splay Further
				if (x.parent != None):
					if x.parent.left == grandparent:
						x.parent.left = x
					else:
						x.parent.right = x
					SplayTree.splay(T,x)
				else:
					T.root = x
				
			elif (grandparent.right == parent and parent.left == x):
				grandparent.right = x.left
				if (grandparent.right != None):
					grandparent.right.parent = grandparent
				parent.left = x.right
				if (parent.left != None):
					parent.left.parent = parent
				
				x.parent = grandparent.parent
				parent.parent = x
				grandparent.parent = x
				
				x.left = grandparent
				x.right = parent
				
				#update size
				grandparent.base = grandparent.update()
				parent.base = parent.update()
				x.base = x.update()
				
				#Splay Further
				if (x.parent != None):
					if x.parent.left == grandparent:
						x.parent.left = x
					else:
						x.parent.right = x
					SplayTree.splay(T, x)
				else:
					T.root = x
			
			else:
				print "Error"

######################################################################
###################				Ordered Table						####################
######################################################################

class OrderedTable(object):
	
	@staticmethod
	def create_table():
		return SplayTree.create_tree(OrderedTable.update, OrderedTable.base())
	
	@staticmethod
	def base():
		return 0
	
	@staticmethod
	def update(par,a,b):
		if (a == None and b == None):
			return 1
		elif (a == None):
			return b.base + 1
		elif (b == None):
			return a.base + 1
		else:
			return a.base + b.base + 1
		
	@staticmethod
	def add(T, key, val):
		return SplayTree.insert(T, key, val)
	
	@staticmethod
	def find(T, key):
		result = SplayTree.find(T,key)
		if (result == None):
			return None
		else:
			return result.data
	
	@staticmethod
	def remove(T, key):
		return SplayTree.delete(T, key)
	
	@staticmethod
	def keys(T, key):
		return SplayTree.getKeys(T)
		
	@staticmethod
	def merge(T1, T2):
		return SplayTree.join(T1, T2)
	
	@staticmethod	
	def value(T):
		return SplayTree.value(T)
	
	@staticmethod
	def range(T, lo, hi):
		(Tl, Th) = SplayTree.split(T,lo)
		(Tmid, Th) = SplayTree.split(Th, hi)
		v = Tmid.base
		return (SplayTree.join(SplayTree.join(Tl, Tmid)), v)
	
	@staticmethod
	def prev(T, x):
		SplayTree.find(T,x)
		if (T.root != None and T.root.left != None):
			return T.root.left.data
	
	@staticmethod
	def next(T,x):
		SplayTree.find(T,x)
		if (T.root != None and T.root.right != None):
			return T.root.right.data

	@staticmethod
	def str(T):
		tree_str = SplayTree.str(T)
		result = "Ordered Set\n"
		result += "Value: %s\n" % (SplayTree.value(T))
		result += "Tree:    \n"
		result += tree_str
		result += "\n"
		return result

class IntervalTable(OrderedTable):
	
	@staticmethod
	def create_table():
		return SplayTree.create_tree(IntervalTable.update, IntervalTable.base())
	
	@staticmethod
	def base():
		return 0
	
	@staticmethod
	def update(par, a,b):
		if (a == None and b == None):
			return par.data[1]
		elif (a == None):
			return max(par.data[1], b.base)
		elif (b == None):
			return max(par.data[1], a.base)
		else:
			return max(par.data[1], a.base, b.base)
			
	@staticmethod
	def add(T, i_lo, i_hi):
		return OrderedTable.add(T, i_lo, [i_lo, i_hi])
	
	@staticmethod
	def find(T, lo, hi):
		print "Hello"
	
	@staticmethod
	def remove(T, lo, high):
		return OrderedTable.remove(T, lo)
	
def test():
	T = IntervalTable.create_table()
	print IntervalTable.str(T)
	interval = [random.randint(0,100) for i in xrange(20)]
	interval2 = [random.randint(0,100) for i in xrange(20)]	
	
	totals = []
	
	for i in xrange(len(interval)):
		iH = max(interval[i], interval2[i])
		iL = min(interval[i], interval2[i])
		totals = [(iL, iH)]
		
	totals = sorted(totals)
	for i in totals:
		total = 0
	
	print IntervalTable.find(T, 3, 20)
	
test()