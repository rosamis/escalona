import grafo
import sys
import transacao as t
import conflito
import visao

def le_arquivo():
    """
    Função que lê arquivo e retorna lista de objetos em que cada objeto contem: tempo_chegada,id,operacao e atributo
    """
    inFile = sys.argv[1]

    with open(inFile,'r') as i:
        linhas = i.readlines()
    lista_transacoes = [t.Transacao(i.split(' ')) for i in linhas]

    return lista_transacoes

def main():
    """
    Função principal da aplicação.
    """
    lista_transacoes = le_arquivo()
    
    lista_saidas = conflito.serializacao_conflito(lista_transacoes)
    visao.equivalencia_visao(lista_transacoes)
    #print(lista_saidas)
    #outFile = sys.argv[2]
    #print(outFile)

if __name__ == "__main__":
    main()