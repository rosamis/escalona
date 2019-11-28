## @package visao
#  Este arquivo contém as funções que determinarão se um escalonamento é equivalente por visão ou não.
#  Trabalho desenvolvido para fins da disciplina de Banco de Dados, feito por Roberta Samistraro Tomigian.

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

## Função que pega a primeira leitura de um escalonamento.
#  @param escalonamento É uma lista de transações que contém todas as transações de um escalonamento.
#  @return Tupla que contém o id da transação, a operação realizada e o atributo.
def primeira_leitura(escalonamento):
    for i in escalonamento:
        if i.operacao == 'R':
            return (i.id, i.operacao, i.atributo)

## Função que verifica se a primeira transação de leitura do agendamento s também é a primeira transação de leitura do agendamento s1.
#  @param escalonamento_s É uma lista de agendamento que contém todas as transações originais e consistentes com o que foi lido do arquivo.
#  @param escalonamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return True caso a primeira leitura do escalonamento s seja igual a primeira leitura do escalonamento s1, e retorna False caso contrário.
def primeira_leitura_igual(escalonamento_s,escalonamento_s1):
    s = primeira_leitura(escalonamento_s)
    s1 = primeira_leitura(escalonamento_s1)
    if s != s1:
        return False
    return s == s1

## Função que percorre a lista que contém as transações filtradas e retorna a transação.
#  @param operacao É a operação a ser buscada e pode ser R ou W.
#  @param lista_filtrados É a lista que contém as transações apenas de read e write que interessam.
#  @return Retorna o objeto transação encontrado.
def pega_elemento(operacao,lista_filtrados):
    for l in lista_filtrados:
        if l.operacao == operacao:
            return l

## Função que procura no escalonamento s1 se a operação de leitura antes da escrita se manteve.
#  @param ti É a transação de leitura
#  @param tj É a transação de escrita
#  @param escalonamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return Retorna True se a leitura antes de escrita se manteve em s1 e False caso contrário.
def procura_em_s1(ti,tj,escalonamento_s1):
    # Filtra as transações que correspondem a ti e tj no escalonamento s1.
    lista_filtrados = list(filter(lambda e: ((e.id == ti.id and e.operacao == ti.operacao and e.atributo == ti.atributo) or (e.id == tj.id
     and e.operacao == tj.operacao and e.atributo == tj.atributo)),escalonamento_s1)) 

    r = pega_elemento("R",lista_filtrados)
    w = pega_elemento("W",lista_filtrados)

    return r.tempo_chegada < w.tempo_chegada

## Função que para cada escrita após leitura do escalonamento s procura no escalonamento s1 para ver se a escrita permanece após a leitura.
#
#  Isso é válido para transações distintas, de mesma operação e mesmo atributo.
#  
#  @param escalonamento_s É uma lista de agendamento que contém todas as transações originais e consistentes com o que foi lido do arquivo.
#  @param escalonamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return Retorna True caso a ordem se mantenha e False caso contrário.
def escrita_apos_leitura(escalonamento_s,escalonamento_s1):
    lista_passados = []
    # Percorre s, acha read e procura write nos passados, se achou, passa como parametro para procurar no s1
    for tj in escalonamento_s:
        if tj.operacao == 'W':
            for ti in lista_passados:
                if ti.id != tj.id and ti.operacao == 'R' and tj.atributo == ti.atributo:
                    if(not procura_em_s1(ti,tj,escalonamento_s1)):
                        return False
        lista_passados.append(tj)
    return True

## Função que pega a última escrita de um escalonamento.
#  @param escalonamento É uma lista de transações que contém todas as transações de um escalonamento.
#  @return Tupla que contém o id da transação, a operação realizada e o atributo.
def ultima_escrita(escalonamento):
    for i in reversed(escalonamento):
        if i.operacao == 'W':
            return (i.id, i.operacao, i.atributo)

## Função que verifica se a última transação de escrita do agendamento s também é a última transação de escrita do agendamento s1.
#  @param escalonamento_s É uma lista de agendamento que contém todas as transações originais e consistentes com o que foi lido do arquivo.
#  @param escalonamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return True caso a última escrita do escalonamento s seja igual a última escrita do escalonamento s1, e retorna False caso contrário.
def ultima_escrita_igual(escalonamento_s,escalonamento_s1):
    s = ultima_escrita(escalonamento_s)
    s1 = ultima_escrita(escalonamento_s1)
    if s != s1:
        return False
    return s == s1

## Função que verifica se todas as transações do agendamento s estão no agendamento s1.
#  @param escalonamento_s É uma lista de agendamento que contém todas as transações originais e consistentes com o que foi lido do arquivo.
#  @param escalonamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return boolean Retorna False caso tenha alguma transação que está no agendamento s mas não está no agendamento s1. Retorna True caso todas as transações do agendamento s estejam no agendamento s1.
def mesmas_transacoes(escalonamento_s,escalonamento_s1):
    for i in escalonamento_s:
        if (not any((x.id == i.id and x.atributo == i.atributo and x.operacao == i.operacao) for x in escalonamento_s1)):
            return False
    return True

## Função que verifica se um agendamento corresponde a todas as exigências, se sim, ele é equivalente por visão e retorna True, se não retorna False.
#  As verificações feitas pela função são:
#
#  - Detecta se o agendamento s1 possui as mesmas transações do agendamento s.
#
#  - Detecta se o último w do agendamento s também é o último w do agendamento s1.
#
#  - Detecta se para cada leitura antes de escrita do agendamento s se mantém no agendamento s1.
#
#  - Detecta se a primeira leitura do agendamento s é a primeira leitura do agendamento s1.
#
#  Se uma dessas alternativas for falsa, ele não é equivalente por visão. Caso contrário, se todas as alternativas forem verdadeiras, ele é equivalente por visão.
#
#  @param lista_agendamento_s É uma lista de agendamento que contém todas as transações originais e consistentes com o que foi lido do arquivo.
#  @param lista_agendamento_s1 É uma lista de agendamento que contém as transações na ordem serial, determinada pela permutação.
#  @return boolean True caso seja passe por todos os testes e False se não.
def verifica_visao(lista_agendamento_s, escalonamento_s1):
    escalonamento_s = copy.deepcopy(lista_agendamento_s)

    if(mesmas_transacoes(escalonamento_s,escalonamento_s1) and ultima_escrita_igual(escalonamento_s,escalonamento_s1) and primeira_leitura_igual(escalonamento_s,escalonamento_s1) and escrita_apos_leitura(escalonamento_s,escalonamento_s1)):
        return True
    return False

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

        

