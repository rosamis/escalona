## @package escalona
#  Este arquivo contém as funções main, leitura e escrita de arquivo.
#  Trabalho desenvolvido para fins da disciplina de Banco de Dados, feito por Roberta Samistraro Tomigian.

import grafo
import sys
import transacao as t
import conflito
import visao
import copy

## Função que recebe a lista de agendamento lida do arquivo e separa as transações de modo que obtenha uma lista que guarda uma lista com os escalonamentos.
#  Em que, cada escalonamento possui todas as operações de transações que estão operando juntas, isto é, que rodam em paralelo até o commit de ambas.
#
#  @return lista_escalona É uma lista de lista de objetos que guarda para cada escalonamento suas transações.
#  @param lista_agendamento_s É o agendamento lido do arquivo de entrada.
def lista_escalona(lista_agendamento_s):
    lista_transacoes = copy.deepcopy(lista_agendamento_s)
    lista_commit = [t for t in lista_transacoes if t.operacao == 'C']
    transacoes_atuais = []
    lista_escalona = []
    lista_aux =  []
    for transacao in lista_transacoes:
        if transacao.id not in transacoes_atuais:
            transacoes_atuais.append(transacao.id)
        if transacao in lista_commit:
            transacoes_atuais.remove(transacao.id)
        lista_aux.append(transacao)
        if len(transacoes_atuais) == 0:
            lista_escalona.append(lista_aux)
            lista_aux = []

    return lista_escalona

## Função que lê arquivo e retorna lista de objetos, que são os agendamentos, em que cada objeto contém: tempo de chegada, id da transação, operação e atributo.
#  
#  @return lista_agendamento_s É a lista de objetos que guarda os dados de cada transação.
def le_arquivo():
    inFile = sys.stdin
    linhas = inFile.readlines()
    lista_agendamento_s = [t.Transacao(i.split(' ')) for i in linhas]
    return lista_agendamento_s

## Função que recebe uma lista, que contém todos os resultados obtidos com a execução do programa, e escreve no arquivo de saida.
#
#  @param lista_saidas É uma lista de string em que cada string guarda o resultado de cada escalonamento.
def escreve_arquivo(lista_saidas):
    outFile = sys.stdout
    for l in lista_saidas:
        outFile.write(l)
        outFile.write("\n")

## Função que recebe o grafo gerado pelo escalonamento, verifica se ele tem ciclo e se tiver, classifica como 'NS'. Além disso, a função recebe o id do escalonamento e 
#  se a função é equivalente por visão ou não e o classifica como SV ou NV respectivamente. A função retorna uma string no formato: 1 1,3,2 NS NV. Em que, o primeiro campo
#  é o id do escalonamneto, o segundo a lista de id das transações presentes no escalonamento, o terceiro se ele é serializável e o quarto se ele é equivalente por visão.
#
#  @return string Guarda o resultado do escalonamento.
#  @param grafo É uma classe utilizada para detectar se o escalonamento é serializável ou não.
#  @param id_escalonamento É um int que guarda o id do escalonamento atual. 
#  @param e É um campo boolean que guarda se o escalonamento é equivalente por visão ou não.
def gera_saida(grafo,id_escalonamento,e):
    if grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' +'NS' + ' ' +'SV'
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'SS' + ' ' + 'NV'
    elif grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'NS' + ' ' + 'NV'
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'SS' + ' ' + 'SV'

## Função que para cada escalonamento da lista verifica se ele é serializável e equivalente por visão. Cada resultado do escalonamento será guardado como string na lista 
#  de saída, que será o retorno da função.
#
#  @return lista_saidas É a lista em que cada nodo contém a saida de um escalonamento.
#  @param lista_escalonados Contém uma lista de lista de escalonamento.
def conflito_escalonamento(lista_escalonados):
    lista_saidas = []
    id_escalonamento = 1
    for escalonamento in lista_escalonados:
        g = conflito.seriabilidade(escalonamento)
        e = visao.equivalencia_visao(escalonamento)
        lista_saidas.append(gera_saida(g,id_escalonamento,e))
        id_escalonamento += 1
    return lista_saidas

## Função principal da aplicação. Ela realiza a leitura, os cálculos e escreve no arquivo.
def main():    
    lista_agendamento_s = le_arquivo()
    lista_escalonados = lista_escalona(lista_agendamento_s)
    lista_saidas = conflito_escalonamento(lista_escalonados)
    escreve_arquivo(lista_saidas)