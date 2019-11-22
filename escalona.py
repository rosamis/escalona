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
        #print("-------------------------------------------")
        #print("transacao atual = ", transacao)
        #print("transacoes_atuais = ", transacoes_atuais)
        # print(lista_commit)
        #print("Lista AUX = ", lista_aux)
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
    inFile = sys.argv[1]

    with open(inFile,'r') as i:
        linhas = i.readlines()
    lista_agendamento_s = [t.Transacao(i.split(' ')) for i in linhas]

    return lista_agendamento_s

def main():
    """
    Função principal da aplicação.
    """
    lista_agendamento_s = le_arquivo()
    #visao.imprime_transacao(lista_agendamento_s)
    lista_escalonados = lista_escalona(lista_agendamento_s)
    #visao.imprime_lista(lista_escalonados)
    lista_saidas = conflito.conflito_escalonamento(lista_escalonados)
    #print(id(lista_agendamento_s))
    
    #visao.equivalencia_visao(lista_agendamento_s)
    #print(lista_saidas)
    #outFile = sys.argv[2]
    #print(outFile)

if __name__ == "__main__":
    main()