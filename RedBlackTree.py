#http://scienceblogs.com/goodmath/2008/05/28/the-basic-balanced-search-tree/
# Par Mark C. Chu-Carroll et modifié par Tristan Savaria

class RedBlackTree(object):
	def __init__(self):
		self._tree = None
		self.count = 0
		
	def Count(self):
		return self.count

	def Insert(self, key, value):
		if self._tree == None:
			self._tree = RedBlackTreeNode(key,value)
			self._tree.SetColor("Black")
		else:
			self._tree = self._tree.Insert(key,value)
		self.count += 1
			
	def Find(self, key):
		return self._subtree_search(self._tree, key)
		
	def Remove(self, key):
		node = self._subtree_search(self._tree, key)
		node._remove(key)
		self.count -= 1

	
	def _subtree_search( self, node, key ):
		if key == node.getKey():
			return node
		elif key < node.getKey():
			if node._left is not None:
				return self._subtree_search( node._left, key )
		else:
			if node._right is not None:
				return self._subtree_search( node._right, key )
		return None
		
	# N complexity, because you need to search the entire Tree if you want to delete a gold-Less Leprechaun in the (i, xi) Tree. Makes sense, right?
	def _HORRIBLE_TP_RELATED_SEARCH( self, node, value ):
		if value == node.getValue():
			return node
		elif node._left is not None:
				return self._subtree_search( node._left, key )
		else:
			if node._right is not None:
				return self._subtree_search( node._right, key )
		return None

	def Print(self):
		if self._tree == None:
			print ("Empty")
		else:
			self._tree.Print(1)
			


class RedBlackTreeNode(object):
	def __init__(self, key, value):
		self._left = None
		self._right = None
		self._value = value
		self._key = key
		self.SetColor("Red")
		self._parent = None
		
	def _remove(self, key):
		if key < self._key:
			self.GetLeft()._remove(key)
		elif key > self._key:
			self.GetRight()._remove(key)
		else:
		
			# 2 children
			if self.GetLeft() and self.GetRight():
				r = self.GetRight().find_min()
				self._key = r.getKey()
				self._value = r.getValue()
				r._remove(r.getKey())
			#Have left Child
			elif self.GetLeft():
				child = self.GetLeft()
				self._replace(self, child)
			#Have right Child
			elif self.GetRight():
				child = self.GetRight()
				self._replace(self, child)
			
			#Node with no children
			else :
				t = self.GetParent()
				if t.GetLeft().getKey() == self.getKey():
					t.SetLeft(None)
				elif t.GetRight().getKey() == self.getKey():
					t.SetRight(None)
				self.SetParent(None)
				
			self.Rebalance()
				
		
		
	
	
	def _replace(self, oldNode, newNode):
		#old = self._subtree_search(self._tree, key)
		#if old is not None:
		oldNode._key = newNode.getKey()
		oldNode._value = newNode.getValue()
		#oldNode.SetColor(newNode.GetColor())
		oldNode.SetColor("Black")
		oldNode.SetLeft(newNode.GetLeft())
		oldNode.SetRight(newNode.GetRight())
		return oldNode
		
	def __lt__(self, other):
		if isinstance(other, self):
			return self.getKey() == other.getKey()
		return false
		
	def find_min(self):   # Gets minimum node (leftmost leaf) in a subtree
		current_node = self
		while current_node.GetLeft():
			current_node = current_node.GetLeft()
		return current_node
		
	def find_max(self):   # Gets maximum node (rightmost leaf) in a subtree
		current_node = self
		while current_node.GetRight():
			current_node = current_node.GetRight()
		return current_node
		
	def num_children(self, node):
		count = 0
		if node.GetLeft() is not None:
			count += 1
		if node.GetRight() is not None:
			count += 1
		return count

	def GetParent(self):
		return self._parent
	
	def getKey(self):
		return self._key
	
	def getValue(self):
		return self._value

	def SetParent(self, parent):
		self._parent = parent

	def GetColor(self):
		return self._color

	def SetColor(self, color):
		self._color = color

	def GetLeft(self):
		return self._left

	def SetLeft(self, left):
		self._left = left

	def GetRight(self):
		return self._right

	def SetRight(self, right):
		self._right = right

	def GetGrandParent(self):
		if self.GetParent() != None:
			return self.GetParent().GetParent()
		else:
			return None

	def GetUncle(self):
		grand = self.GetGrandParent()
		if grand is not None:
			if grand.GetLeft() == self.GetParent():
				return grand.GetRight()
			else:
				return grand.GetLeft()
		else:
			return None
	
	def Rebalance(self):     
		# WP case 1: tree root
		if self.GetParent() is None:
			self.SetColor("Black")
			return self
		# WP case 2: The parent of the target node is BLACK,
		#   so the tree is in fine balance shape; just return the
		#   tree root
		if self.GetParent().GetColor() == "Black":
			return self.GetRoot()
		# From here on, we know that parent is Red.
		# WP Case 3:  self, parent, and uncle are all red.
		if self.GetUncle() is not None and self.GetUncle().GetColor() == "Red":
			self.GetUncle().SetColor("Black")
			self.GetParent().SetColor("Black")
			self.GetGrandParent().SetColor("Red")
			return self.GetGrandParent().Rebalance()
		# By now, we know that self and parent are red; and the uncle is black.
		# We also know that the grandparent is not None, because if it were, the
		# parent would be root, which must be black. So this means that we 
		# need to do a pivot on the parent
		return self.PivotAndRebalance()

	def GetRoot(self):
		if self.GetParent() is None:
			return self
		else:
			return self.GetParent().GetRoot()


	def PivotAndRebalance(self):
		# First, distinguish between the case where where my parent is
		# a left child or a right child.
		if self.GetGrandParent().GetLeft() == self.GetParent():
			if self.GetParent().GetRight() == self:
				# WP case 4: I'm the right child of my parent, and my parent is the
				# left child of my grandparent. Pivot right around me.
				return self.PivotLeft(False)
			else:
				# WP case 5
				# If I'm the left child, and my parent is the left child, then
				# pivot right around my parent.
				return self.GetParent().PivotRight(True)
		else: # My parent is the right child.
			if self.GetParent().GetLeft() == self:
				# WP case 4, reverse.
				return self.PivotRight(False)
			else:
				# WY case 5 reverse
				return self.GetParent().PivotLeft(True)


	def PivotRight(self, recolor):
		# Hurrah, I'm going to be the new root of the subtree!
		left = self.GetLeft()
		right = self.GetRight()
		parent = self.GetParent()
		grand = self.GetGrandParent()
		# move my right child to be the left of my soon-to-be former parent.
		parent.SetLeft(right)
		if right is not None:
			right.SetParent(parent)
		# Move up, and make my old parent my right child.
		self.SetParent(grand)
		if grand is not None:
			if  grand.GetRight()  == parent:
				grand.SetRight(self)
			else:
				grand.SetLeft(self)
		self.SetRight(parent)
		parent.SetParent(self)
		if recolor is True:
			parent.SetColor("Red")
			self.SetColor("Black")
			return self.GetRoot()
		else:
			# rebalance from the new position of my former parent.
			return parent.Rebalance()

	def PivotLeft(self, recolor):
		# Hurrah, I'm going to be the new root of the subtree!
		left = self.GetLeft()
		right = self.GetRight()
		parent = self.GetParent()
		grand = self.GetGrandParent()
		# move my left child to be the right of my soon-to-be former parent.
		parent.SetRight(left)
		if left is not None:
			left.SetParent(parent)
		# Move up, and make my old parent my right child.
		self.SetParent(grand)
		if grand is not None:
			if  grand.GetRight() == parent:
				grand.SetRight(self)
			else:
				grand.SetLeft(self)
		self.SetLeft(parent)
		parent.SetParent(self)
		if recolor is True:
			parent.SetColor("Red")
			self.SetColor("Black")
			return self.GetRoot()
		else:
			# rebalance from the position of my former parent.
			return parent.Rebalance()


	def Insert(self, key, value):
		if self.getKey() > key:
			if self.GetLeft() is None:
				self.SetLeft(RedBlackTreeNode(key, value))
				self.GetLeft().SetParent(self)
				return self.GetLeft().Rebalance()
			else:
				return self.GetLeft().Insert(key, value)
		else:
			if self.GetRight() is None:
				self.SetRight(RedBlackTreeNode(key, value))
				self.GetRight().SetParent(self)
				return self.GetRight().Rebalance()        
			else:
				return self.GetRight().Insert(key, value)


	def Print(self, indent = 1):
		for i in range(indent):
			print ("  ", end=" ")
		print ("%s (%s)(%s)" % (self.getKey(), self.GetColor(), self.getValue()))
		if self.GetLeft() is None:
			for i in range(indent+1):
				print ("  ", end=" ")
			print ("None(Black)")
		else:
			self.GetLeft().Print(indent+1)
		if self.GetRight() is None:
			for i in range(indent+1):
				print ("  ", end=" ")
			print ("None(Black)")
		else:
			self.GetRight().Print(indent+1)
			
			
				
				