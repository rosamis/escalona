## @package conflito
#  Este arquivo contém a função que calcula se um escalonamento é serializável ou não.
#  Trabalho desenvolvido para fins da disciplina de Banco de Dados, feito por Roberta Samistraro Tomigian.

import grafo
import visao
import copy

## Função que recebe um escalonamento e adiciona arestas em um grafo direcionado para cada condição satisfeita.
#  A função adicionará aresta no grafo para mesmo atributo, mesma operação e em transações distintas nos seguintes casos:   
#
#  - Leitura após escrita.
#
#  - Escrita após leitura.
#
#  - Escrita após escrita.
#
#  @param escalonamento É uma lista de objeto que guarda o tempo de chegada, id, operação e atributo de cada transação.
#  @return g É um grafo que contém como vértice todos os id do escalonamento e as arestas encontradas na função, se existirem.

def seriabilidade(escalonamento):
    lista_passados = []
    g = grafo.Grafo("serial")
    for tj in escalonamento:
        # Adiciona vertices no grafo
        if tj.id not in g.vertices:
            g.add_vertice(tj.id)

        # Detecta leitura após escrita
        if tj.operacao == 'R':
            for ti in lista_passados:
                if ti.id != tj.id and ti.operacao == 'W' and tj.atributo == ti.atributo:
                    g.conectar(ti.id,tj.id)

        # Detecta escrita após leitura
        if tj.operacao == 'W':
            for ti in lista_passados:
                if ti.id != tj.id and ti.operacao == 'R' and tj.atributo == ti.atributo:
                    g.conectar(ti.id,tj.id)   

        # Detecta escrita após escrita
        if tj.operacao == 'W':
            for ti in lista_passados:
                if ti.id != tj.id and ti.operacao == 'W' and tj.atributo == ti.atributo:
                    g.conectar(ti.id,tj.id) 

        lista_passados.append(tj)
    return g



