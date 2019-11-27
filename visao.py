import itertools
import conflito
import copy

def imprime_lista(lista):
    for t in lista:
        print("\n")
        imprime_transacao(t)

def imprime_transacao(lista):
    for i in lista:
        print(i.tempo_chegada,i.id,i.operacao,i.atributo)

def lista_permuta(lista_id):
    return list(itertools.permutations(lista_id))

def separa_listas(lista_agendamento_s):
    lista_id = []
    dicionario_t = {}
    lista = copy.deepcopy(lista_agendamento_s)
    for s in lista:
        if s.id not in lista_id:
            lista_id.append(s.id)
            x = [t for t in lista if t.id == s.id]
            dicionario_t.update({s.id:x}) 

    return dicionario_t, lista_id
    
def cria_lista_s1(permuta, dicionario_t):
    lista_agendamento_s1 = []
    tempo_chegada = 1
    for p in permuta:
        d = dicionario_t[p]
        for dados in d:
            dados.tempo_chegada = tempo_chegada
            lista_agendamento_s1.append(dados)
            tempo_chegada += 1

    return lista_agendamento_s1
    
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
    lista_filtrados = list(filter(lambda e: ((e.id == ti.id and e.operacao == ti.operacao and e.atributo == ti.atributo) or (e.id == tj.id
     and e.operacao == tj.operacao and e.atributo == tj.atributo)),escalonamento_s1)) 

    r = pega_elemento("R",lista_filtrados)
    w = pega_elemento("W",lista_filtrados)

    return r.tempo_chegada < w.tempo_chegada

def leitura_apos_escrita(escalonamento_s,escalonamento_s1,atributos):
    lista_passados = []
    # percorre s, acha read e procura write nos passados, se achou, passa como parametro para procurar no s1
    for tj in escalonamento_s:
        # Detecta escrita após leitura
        if tj.operacao == 'W':
            for ti in lista_passados:
                if ti.id != tj.id and ti.operacao == 'R' and tj.atributo == ti.atributo:
                    if(not procura_em_s1(ti,tj,escalonamento_s1)):
                        return False
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
    # Detecta se possui as mesmas transações
    # Detecta se o último w de S também é de S1
    # Detecta se tem consistencia entre leitura antes de escrita ou não
    if(mesmas_transacoes(escalonamento_s,escalonamento_s1) and ultima_escrita_igual(escalonamento_s,escalonamento_s1,atributos) and primeira_leitura_igual(escalonamento_s,escalonamento_s1,atributos) and leitura_apos_escrita(escalonamento_s,escalonamento_s1,atributos)):
        return True

def equivalencia_visao(escalonamento):
    dicionario_t, lista_id = separa_listas(escalonamento)
    permutas = lista_permuta(lista_id)
    for p in permutas:
        escalonamento_s1 = cria_lista_s1(p, dicionario_t)
        if(verifica_visao(escalonamento,escalonamento_s1)):
            return True
    return False

        

