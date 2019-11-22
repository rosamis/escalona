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
       

#def equivalencia_visao(lista_escalonados):
    #print(id(lista_agendamento_s))
    #dicionario_t, lista_id = separa_listas(lista_agendamento_s)
    #lista_p = lista_permuta(lista_id)
    #imprime_transacao(lista_agendamento_s)
    #print("\n")
        #imprime_transacao(lista_agendamento_s)
        #imprime_lista(lista_escalonamento)
    #for permuta in lista_p:
        #print(permuta)
    #    lista_agendamento_s1 = cria_lista_s1(permuta,dicionario_t)
        #lista_escalonamento = conflito.lista_escalona(lista_agendamento_s1)
        #imprime_transacao(lista_agendamento_s1)
#    return
        #print("\n")
        #print(lista_escalonamento)
        #print(lista_escalonamento[1][2].tempo_chegada)
        #print(lista_agendamento_s1[5].atributo)

    #for escalonamento in lista_escalonados:

        

