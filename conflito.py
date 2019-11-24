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

def leitura_apos_escrita(escalonamento_s,escalonamento_s1):
    return True

def ultima_escrita(escalonamento):
    for i in reversed(escalonamento):
        if i.operacao == 'W':
            return (i.id, i.operacao, i.atributo)

def ultima_escrita_igual(escalonamento_s,escalonamento_s1):
    s = ultima_escrita(escalonamento_s)
    s1 = ultima_escrita(escalonamento_s1)
    return s==s1

def mesmas_transacoes(escalonamento_s,escalonamento_s1):
    return True

def verifica_visao(lista_agendamento_s, escalonamento_s1):
    escalonamento_s = copy.deepcopy(lista_agendamento_s)
    #visao.imprime_transacao(escalonamento_s)
    # Detecta se possui as mesmas transações
    # Detecta se o último w de S também é de S1
    # Detecta se tem consistencia entre leitura após escrita ou não
    if(leitura_apos_escrita(escalonamento_s,escalonamento_s1) and ultima_escrita_igual(escalonamento_s,escalonamento_s1) and mesmas_transacoes(escalonamento_s,escalonamento_s1)):
        print("entrou")

def equivalencia_visao(escalonamento):
    #visao.imprime_transacao(escalonamento)
    print("\n")
    dicionario_t, lista_id = visao.separa_listas(escalonamento)
    permutas = visao.lista_permuta(lista_id)
    #print(permutas)
    for p in permutas:
        escalonamento_s1 = visao.cria_lista_s1(p, dicionario_t)
        #print("escalona s\n")
        #visao.imprime_transacao(escalonamento)
        #print("\n")
        #print("escalona s1\n")
        #visao.imprime_transacao(escalonamento_s1)
        print("\n")
        #print(p)
        verifica_visao(escalonamento,escalonamento_s1)
        return


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