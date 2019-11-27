import grafo
import sys
import transacao as t
import conflito
import visao
import copy

def lista_escalona(lista_agendamento_s):
    """
    Lista que guarda listas com os escalonamentos
    """
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

def le_arquivo():
    """
    Função que lê arquivo e retorna lista de objetos em que cada objeto contem: tempo_chegada,id,operacao e atributo
    """
    inFile = sys.stdin
    linhas = inFile.readlines()
    lista_agendamento_s = [t.Transacao(i.split(' ')) for i in linhas]

    return lista_agendamento_s

def escreve_arquivo(lista_saidas):
    outFile = sys.stdout

    for l in lista_saidas:
        outFile.write(l)
        outFile.write("\n")

def gera_saida(grafo,id_escalonamento,e):
    if grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' +'NS' + ' ' +'SV'
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'SS' + ' ' + 'NV'
    elif grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'NS' + ' ' + 'NV'
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return str(id_escalonamento) + ' ' + ','.join(str(e) for e in grafo.vertices) + ' ' + 'SS' + ' ' + 'SV'

def conflito_escalonamento(lista_escalonados):
    lista_saidas = []
    id_escalonamento = 1
    for escalonamento in lista_escalonados:
        g = conflito.seriabilidade(escalonamento)
        e = visao.equivalencia_visao(escalonamento)
        lista_saidas.append(gera_saida(g,id_escalonamento,e))
        id_escalonamento += 1
    return lista_saidas

def main():
    """
    Função principal da aplicação.
    """
    lista_agendamento_s = le_arquivo()
    lista_escalonados = lista_escalona(lista_agendamento_s)
    lista_saidas = conflito_escalonamento(lista_escalonados)
    escreve_arquivo(lista_saidas)