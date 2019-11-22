import grafo
import visao
import copy
        
def gera_saida(grafo,id_escalonamento):
    if grafo.verificar_ciclos(grafo.vertices[0]):
        return (id_escalonamento,grafo.vertices,'NS')
    else:
        return (id_escalonamento,grafo.vertices,'SS')

def seriabilidade(escalonamento):
    lista_passados = []
    g = grafo.Grafo("serial")
    #print("\n")
    for tj in escalonamento:
        #print(tj.tempo_chegada,tj.id,tj.operacao,tj.atributo)
        #print(transacao.tempo_chegada,transacao.id,transacao.operacao,transacao.atributo)
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

def verifica_visao(escalonamento_s, escalonamento_s1):
    lista_agendamento_s = copy.deepcopy(escalonamento_s)
    #visao.imprime_transacao(escalonamento_s1)

def equivalencia_visao(escalonamento):
    #visao.imprime_transacao(escalonamento)
    print("\n")
    dicionario_t, lista_id = visao.separa_listas(escalonamento)
    permutas = visao.lista_permuta(lista_id)
    print(permutas)
    for p in permutas:
        escalonamento_s1 = visao.cria_lista_s1(p, dicionario_t)
        visao.imprime_transacao(escalonamento_s1)
        print("\n")
        verifica_visao(escalonamento,escalonamento_s1)
        # Detecta se possui as mesmas transações
        # Detecta se o último w de S também é de S1
        # Detecta se tem consistencia entre leitura após escrita ou não

def conflito_escalonamento(lista_escalonados):
    #visao.imprime_transacao(lista_escalonados)
    lista_saidas = []
    id_escalonamento = 1
    for escalonamento in lista_escalonados:
        #visao.imprime_transacao(escalonamento)
        #print("\n")
        g = seriabilidade(escalonamento)
        equivalencia_visao(escalonamento)
        lista_saidas.append(gera_saida(g,id_escalonamento))
        id_escalonamento += 1
    #print (lista_saidas)
    return lista_saidas