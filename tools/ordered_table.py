import splay_tree



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