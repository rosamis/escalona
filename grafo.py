## @package grafo
#  Este arquivo contém a classe Grafo.
#  Trabalho desenvolvido para fins da disciplina de Banco de Dados, feito por Roberta Samistraro Tomigian.

from collections import defaultdict
import copy

## Classe que guarda um grafo.
#
class Grafo():
	## Construtor da classe. Ele recebe uma string e atribui os valores correspondentes para cada atributo da classe.
    #  @param self Ponteiro para o objeto.
    #  @param nome É uma string.
	def __init__(self,nome):
		## É uma string que guarda o nome do grafo.
		self.nome = nome
		## @var _data
   		#  É um dicionário privado que guarda para cada vértice suas arestas que o conecta com outros vértices.
		self._data = defaultdict(list)
		## É uma lista que guarda todos os vértices do grafo.
		self.vertices = []
	
	## Método da classe que adiciona um vértice ao grafo.
    #  @param self Ponteiro para o objeto.
    #  @param n É um int que corresponde ao nome do vértice.
	def add_vertice(self,n):
		self.vertices.append(n)

	## Método da classe que adiciona uma aresta ao grafo.
    #  @param self Ponteiro para o objeto.
    #  @param nodo_origem É um int que corresponde ao nome do vértice que será a origem da aresta.
    #  @param nodo_destino É um int que corresponde ao nome do vértice que será o destino da aresta.
	def conectar(self, nodo_origem, nodo_destino):
		self._data[nodo_origem].append(nodo_destino)

	## Método da classe que retorna a lista de vizinhos de um vértice.
    #  @param self Ponteiro para o objeto.
    #  @param nodo É um int que corresponde ao nome do vértice que se deseja a lista de vizinhos.
    #  @return É uma lista.
	def vizinhos(self, nodo):
		return self._data[nodo]

	## Método da classe que busca ciclo em grafo por meio da busca em profundidade a partir de um vértice inicial.
	#  O programa faz uma busca por todos os vértices e seus vizinhos e vai colocando na lista de nodos visitados, quando encontra um nodo que já está na lista ele retorna  True,
	#  caso não encontre, ele retornará False.
    #  @param self Ponteiro para o objeto.
    #  @param vertice_inicial É int que corresponde ao vértice em que se iniciará a busca por ciclo.
    #  @return É um boolean que se True indica que há ciclo e se False indica que não há ciclo.
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
