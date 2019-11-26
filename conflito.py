import grafo
import visao
import copy
        
def gera_saida(grafo,id_escalonamento,e):
    #print(grafo.verificar_ciclos(grafo.vertices[0]))
    #print(e)
    if grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return (id_escalonamento,grafo.vertices,'NS','SV')
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return (id_escalonamento,grafo.vertices,'SS', 'NV')
    elif grafo.verificar_ciclos(grafo.vertices[0]) and not e:
        return (id_escalonamento,grafo.vertices,'NS', 'NV')
    elif not grafo.verificar_ciclos(grafo.vertices[0]) and e:
        return (id_escalonamento,grafo.vertices,'SS', 'SV')

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

def lista_atributos(escalonamento):
    atributos = []
    for e in escalonamento:
        if e.atributo not in atributos and e.atributo != "-":
            atributos.append(e.atributo)

    return atributos

def primeira_leitura(escalonamento,atributo):
    for i in escalonamento:
        if i.operacao == 'R' and i.atributo == atributo:
            return (i.id, i.operacao, i.atributo)

def primeira_leitura_igual(escalonamento_s,escalonamento_s1,atributos):
    for a in atributos:
        s = primeira_leitura(escalonamento_s,a)
        s1 = primeira_leitura(escalonamento_s1,a)
        if s != s1:
            return False
    return s == s1

def pega_elemento(operacao,lista_filtrados):
    for l in lista_filtrados:
        if l.operacao == operacao:
            return l

def procura_em_s1(ti,tj,escalonamento_s1):
    # print("\nti")
    # print(tj.tempo_chegada,tj.id,tj.operacao,tj.atributo)
    # print("\ntj")
    # print(ti.tempo_chegada,ti.id,ti.operacao,ti.atributo)
    # print("\n")
    lista_filtrados = list(filter(lambda e: ((e.id == ti.id and e.operacao == ti.operacao and e.atributo == ti.atributo) or (e.id == tj.id
     and e.operacao == tj.operacao and e.atributo == tj.atributo)),escalonamento_s1)) 
    # print("\nfilt")
    # visao.imprime_transacao(lista_filtrados)
    r = pega_elemento("R",lista_filtrados)
    w = pega_elemento("W",lista_filtrados)

    # print("\nr")
    # print(r.atributo,r.id,r.operacao,r.tempo_chegada)
    # print(w.atributo,w.id,w.operacao,w.tempo_chegada)
    # print("\n")
    return r.tempo_chegada < w.tempo_chegada

def leitura_apos_escrita(escalonamento_s,escalonamento_s1,atributos):
    lista_passados = []
    # percorre s, acha read e procura write nos passados, se achou, passa como parametro para procurar no s1
    for tj in escalonamento_s:
        # Detecta escrita após leitura
        if tj.operacao == 'W':
            for ti in lista_passados:
                #print(ti.atributo,ti.id,ti.operacao,ti.tempo_chegada)
                if ti.id != tj.id and ti.operacao == 'R' and tj.atributo == ti.atributo:
                    #print('aa')
                    #print(ti.atributo,ti.id,ti.operacao,ti.tempo_chegada)
                    #print(procura_em_s1(ti,tj,escalonamento_s1))
                    #print ("\nfiltro")
                    if(not procura_em_s1(ti,tj,escalonamento_s1)):
                        return False
                    #print ("\nesca")
                    #visao.imprime_transacao(escalonamento_s1)
                    #if(not procura_em_s1(ti,tj,escalonamento_s1)):
                    #    return False
        lista_passados.append(tj)
    return True

def ultima_escrita(escalonamento,atributo):
    for i in reversed(escalonamento):
        if i.operacao == 'W' and i.atributo == atributo:
            return (i.id, i.operacao, i.atributo)

def ultima_escrita_igual(escalonamento_s,escalonamento_s1,atributos):
    for a in atributos:
        s = ultima_escrita(escalonamento_s,a)
        s1 = ultima_escrita(escalonamento_s1,a)
        if s != s1:
            return False
    return s == s1

def mesmas_transacoes(escalonamento_s,escalonamento_s1):
    for i in escalonamento_s:
        if (not any((x.id == i.id and x.atributo == i.atributo and x.operacao == i.operacao) for x in escalonamento_s1)):
            return False
    return True

def verifica_visao(lista_agendamento_s, escalonamento_s1):
    escalonamento_s = copy.deepcopy(lista_agendamento_s)
    atributos = lista_atributos(escalonamento_s)
    #visao.imprime_transacao(escalonamento_s)
    # Detecta se possui as mesmas transações
    # Detecta se o último w de S também é de S1
    # Detecta se tem consistencia entre leitura antes de escrita ou não
    if(mesmas_transacoes(escalonamento_s,escalonamento_s1) and ultima_escrita_igual(escalonamento_s,escalonamento_s1,atributos) and primeira_leitura_igual(escalonamento_s,escalonamento_s1,atributos) and leitura_apos_escrita(escalonamento_s,escalonamento_s1,atributos)):
        return True

def equivalencia_visao(escalonamento):
    #visao.imprime_transacao(escalonamento)
    #print("\n")
    dicionario_t, lista_id = visao.separa_listas(escalonamento)
    permutas = visao.lista_permuta(lista_id)
    for p in permutas:
        escalonamento_s1 = visao.cria_lista_s1(p, dicionario_t)
        #print("escalona s\n")
        #visao.imprime_transacao(escalonamento)
        #print("\n")
        #print("escalona s1\n")
        #visao.imprime_transacao(escalonamento_s1)
        #print("\n")
        #print(p)
        if(verifica_visao(escalonamento,escalonamento_s1)):
            visao.imprime_transacao(escalonamento_s1)
            return True
    return False


def conflito_escalonamento(lista_escalonados):
    #visao.imprime_transacao(lista_escalonados)
    lista_saidas = []
    id_escalonamento = 1
    for escalonamento in lista_escalonados:
        #visao.imprime_transacao(escalonamento)
        #print("\n")
        g = seriabilidade(escalonamento)
        e = equivalencia_visao(escalonamento)
        lista_saidas.append(gera_saida(g,id_escalonamento,e))
        print(lista_saidas)
        id_escalonamento += 1
    #print (lista_saidas)
    return lista_saidas