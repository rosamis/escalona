## @package visao
#  Este arquivo contém as funções que determinarão se um escalonamento é equivalente por visão ou não.

import itertools
import conflito
import copy

## Função auxiliar que imprime uma lista de lista de transações.
#  @param lista É uma lista de lista de transações.
def imprime_lista(lista):
    for t in lista:
        print("\n")
        imprime_transacao(t)

## Função auxiliar que imprime uma lista de transações.
#  @param lista É uma lista de transações.
def imprime_transacao(lista):
    for i in lista:
        print(i.tempo_chegada,i.id,i.operacao,i.atributo)

## Função que calcula a permutação de uma lista de id de transação.
#  @param lista_id É uma lista de id de transações.
#  @return lista que contém tuplas com as permutações de todos os id de transações.
def lista_permuta(lista_id):
    return list(itertools.permutations(lista_id))

## Função que, a partir de uma lista de agendamento s que contém o escalonamento, guarda em um dicionário as transações daquele escalonamento separado por id.
#  @param lista_agendamento_s É uma lista de objeto que guarda o tempo de chegada, id, operação e atributo de cada transação.
#  @return dicionario_t É um dicionário que possui como chave o id da transação e como valor a lista de objetos de todas as transações daquele id da transação. 
#  @return lista_id Guarda a lista que contém todos os ids presentes no escalonamento.
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

## Função que cria o agendamento s1 a partir da ordem da permutação e do dicionário de transações.
#  @param permuta É uma tupla que guarda a permutação. 
#  @param dicionario_t É um dicionário que possui como chave o id da transação e como valor a lista de objetos de todas as transações daquele id da transação. 
#  @return lista_agendamento_s1 É a lista de transações com todas as transações na ordem da permutação.
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

## Função 
#  @param 
#  @return     
def lista_atributos(escalonamento):
    atributos = []
    for e in escalonamento:
        if e.atributo not in atributos and e.atributo != "-":
            atributos.append(e.atributo)

    return atributos

## Função 
#  @param 
#  @return 
def primeira_leitura(escalonamento,atributo):
    for i in escalonamento:
        if i.operacao == 'R' and i.atributo == atributo:
            return (i.id, i.operacao, i.atributo)

## Função 
#  @param 
#  @return 
def primeira_leitura_igual(escalonamento_s,escalonamento_s1,atributos):
    for a in atributos:
        s = primeira_leitura(escalonamento_s,a)
        s1 = primeira_leitura(escalonamento_s1,a)
        if s != s1:
            return False
    return s == s1

## Função 
#  @param 
#  @return 
def pega_elemento(operacao,lista_filtrados):
    for l in lista_filtrados:
        if l.operacao == operacao:
            return l

## Função 
#  @param 
#  @return 
def procura_em_s1(ti,tj,escalonamento_s1):
    lista_filtrados = list(filter(lambda e: ((e.id == ti.id and e.operacao == ti.operacao and e.atributo == ti.atributo) or (e.id == tj.id
     and e.operacao == tj.operacao and e.atributo == tj.atributo)),escalonamento_s1)) 

    r = pega_elemento("R",lista_filtrados)
    w = pega_elemento("W",lista_filtrados)

    return r.tempo_chegada < w.tempo_chegada

## Função 
#  @param 
#  @return 
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

## Função 
#  @param 
#  @return 
def ultima_escrita(escalonamento,atributo):
    for i in reversed(escalonamento):
        if i.operacao == 'W' and i.atributo == atributo:
            return (i.id, i.operacao, i.atributo)

## Função 
#  @param 
#  @return 
def ultima_escrita_igual(escalonamento_s,escalonamento_s1,atributos):
    for a in atributos:
        s = ultima_escrita(escalonamento_s,a)
        s1 = ultima_escrita(escalonamento_s1,a)
        if s != s1:
            return False
    return s == s1

## Função 
#  @param 
#  @return 
def mesmas_transacoes(escalonamento_s,escalonamento_s1):
    for i in escalonamento_s:
        if (not any((x.id == i.id and x.atributo == i.atributo and x.operacao == i.operacao) for x in escalonamento_s1)):
            return False
    return True

## Função 
#  @param 
#  @return 
def verifica_visao(lista_agendamento_s, escalonamento_s1):
    escalonamento_s = copy.deepcopy(lista_agendamento_s)
    atributos = lista_atributos(escalonamento_s)
    # Detecta se possui as mesmas transações
    # Detecta se o último w de S também é de S1
    # Detecta se tem consistencia entre leitura antes de escrita ou não
    if(mesmas_transacoes(escalonamento_s,escalonamento_s1) and ultima_escrita_igual(escalonamento_s,escalonamento_s1,atributos) and primeira_leitura_igual(escalonamento_s,escalonamento_s1,atributos) and leitura_apos_escrita(escalonamento_s,escalonamento_s1,atributos)):
        return True

## Função que calcula para cada permutação de um escalonamento se ele é equivalente por visão ou não.
#  @param escalonamento É uma lista de objeto que guarda o tempo de chegada, id, operação e atributo de cada transação.
#  @return boolean A função retornará True para a primeira permutação de um escalonamento que passar em todos os testes e False caso nenhuma permutação de um escalonamento passe no teste.
def equivalencia_visao(escalonamento):
    dicionario_t, lista_id = separa_listas(escalonamento)
    permutas = lista_permuta(lista_id)
    for p in permutas:
        escalonamento_s1 = cria_lista_s1(p, dicionario_t)
        if(verifica_visao(escalonamento,escalonamento_s1)):
            return True
    return False

        

