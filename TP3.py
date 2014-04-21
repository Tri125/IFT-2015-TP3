#!/usr/bin/env python
# encoding: utf-8
from RedBlackTree import RedBlackTree
import random
"""
TP2.py

Coéquipiers :
Tristan Savaria
"""





def main(n):
	living = n
	starting_gold = 1000000
	RBPosition = RedBlackTree()
	RBGold = RedBlackTree()
	
	#Set up and initial turn
	for x in range(living):
		post = 0 + random.uniform(-1, 1) * starting_gold
		RBGold.Insert(post, starting_gold)
		RBPosition.Insert(x, post)
		
	while living > 2:
		for x in range(living):
			print(living)
			print(x)
			oldPost = RBPosition.Find(x).getValue()
			oldGold = RBGold.Find(oldPost).getValue()
			post = oldPost + random.uniform(-1, 1) * oldGold
			RBGold.Remove(oldPost)
			RBGold.Insert(post, oldGold)
			RBPosition.Remove(x)
			RBPosition.Insert(x, post)
			current = RBGold.Find(post)
			nearest = None
			if current.GetLeft() != None:
				nearest = current.GetLeft().find_max()
			elif current.GetRight() != None:
				nearest = current.GetRight().find_min()
			else:
				nearest = current.GetParent()
			stolen = nearest.getValue() // 2
			nearest._value = stolen
			if nearest.getValue() == 0:
				print("dead")
				living -= 1
				RBGold.Remove(nearest.getKey())
				RBPost.Remove(RBPost._HORRIBLE_TP_RELATED_SEARCH(RBPost.self_tree, nearest.getKey()))
			newGold = current.getValue() + stolen
			print(post)
			RBGold.Remove(post)
			RBGold.Insert(post, newGold)
			if living <= 2:
				break
			
	RBPost.Print()	
	RBGold.Print()
		
		
	
	
	print("al")

	
main(10)