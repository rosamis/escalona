import grafo
import sys

def lista_escalona(lista_transacoes):
    """
    Lista que guarda listas com os escalonamentos
    """
    lista_commit = [t for t in lista_transacoes if t[2] == 'C']
    transacoes_atuais = []
    lista_escalona = []
    lista_aux =  []
    for transacao in lista_transacoes:
        #print("-------------------------------------------")
        #print("transacao atual = ", transacao)
        #print("transacoes_atuais = ", transacoes_atuais)
        # print(lista_commit)
        #print("Lista AUX = ", lista_aux)
        if transacao[1] not in transacoes_atuais:
            transacoes_atuais.append(transacao[1])
        if transacao in lista_commit:
            transacoes_atuais.remove(transacao[1])
        lista_aux.append(transacao)
        if len(transacoes_atuais) == 0:
            lista_escalona.append(lista_aux)
            lista_aux = []
    return lista_escalona
        

def seriabilidade(lista_transacoes):
    lista_escalonados = lista_escalona(lista_transacoes)
    print(lista_escalonados)
    for escalonamento in lista_escalonados:
        lista_vertices = []
        # Adiciona vertices no grafo
        for transacao in escalonamento:
            if transacao[1] not in lista_vertices:
                lista_vertices.append(transacao[1])
        g = grafo.Grafo(lista_vertices)
        print(g.grafo[1])
def le_arquivo():
    """
    Função que lê arquivo e retorna lista de tuplas no formato [(id,transação,tipo,atributo)]
    """
    inFile = sys.argv[1]

    with open(inFile,'r') as i:
        linhas = i.readlines()
    lista_transacoes = [(int(i.split(' ')[0]),int(i.split(' ')[1]),i.split(' ')[2],i.split(' ')[3].split('\n')[0]) for i in linhas]

    return lista_transacoes

def main():
    """
    Função principal da aplicação.
    """
    lista_transacoes = le_arquivo()

    seriabilidade(lista_transacoes)
    #outFile = sys.argv[2]
    #print(outFile)

if __name__ == "__main__":
    main()