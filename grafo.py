from collections import defaultdict
import copy

class Grafo():
	def __init__(self,nome):
		self.nome = nome
		self._data = defaultdict(list)
		self.vertices = []

	def add_vertice(self,n):
		self.vertices.append(n)

	def conectar(self, nodo_origem, nodo_destino):
		self._data[nodo_origem].append(nodo_destino)

	def vizinhos(self, nodo):
		return self._data[nodo]

	def verificar_ciclos(self,vertice_inicial):
		nodos_visitados = set()
		
		nodos_restantes = copy.deepcopy(self._data[vertice_inicial])

		while nodos_restantes:
			nodo_atual = nodos_restantes.pop()
			nodos_visitados.add(nodo_atual)

			for vizinho in self.vizinhos(nodo_atual):
				if vizinho in nodos_visitados:
						return True
				nodos_restantes.append(vizinho)
		return False
