from util import *

class BSTNode(object):
	
	def __init__(self, key,data, parent):
		self.x = key
		self.data = data
		self.parent = parent
		self.left = None
		self.right = None
		
	def __str__(self):
		return "BSTNode(%s)" % (str(self.key))
	
class TreeHeader(object):
	
	def __init__(self, name, size):
		self.name = name
		self.size = size
		self.root = None
		
#---------------- Binary Search Tree -----------------------#

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
	def create_tree():
		return TreeHeader()
	
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
	