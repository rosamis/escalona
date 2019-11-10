# Python program to detect cycle 
# in a grafo 

from collections import defaultdict 

class Grafo(): 
	def __init__(self, vertices): 
		self.grafo = defaultdict(list) 
		self.vertices = vertices 

	def add_aresta(self, u, v): 
		self.grafo[u].append(v) 

	def isCyclicUtil(self, v, visited, recStack): 

		# Mark current node as visited and 
		# adds to recursion stack 
		visited[v] = True
		recStack[v] = True

		# Recur for all vizinhoss 
		# if any vizinhos is visited and in 
		# recStack then grafo is cyclic 
		for vizinhos in self.grafo[v]: 
			if visited[vizinhos] == False: 
				if self.isCyclicUtil(vizinhos, visited, recStack) == True: 
					return True
			elif recStack[vizinhos] == True: 
				return True

		# The node needs to be poped from 
		# recursion stack before function ends 
		recStack[v] = False
		return False

	# Returns true if grafo is cyclic else false 
	def isCyclic(self): 
		visited = [False] * self.V 
		recStack = [False] * self.V 
		for node in range(self.V): 
			if visited[node] == False: 
				if self.isCyclicUtil(node, visited, recStack) == True: 
					return True
		return False
