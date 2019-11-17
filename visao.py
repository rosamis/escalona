import itertools

def lista_permuta(lista_id):

    return list(itertools.permutations(lista_id))

def separa_listas(lista_agendamento_s):
    lista_id = []
    dicionario_t = {}
    for s in lista_agendamento_s:
        if s.id not in lista_id:
            lista_id.append(s.id)
            x = [t for t in lista_agendamento_s if t.id == s.id]
            dicionario_t.update({s.id:x}) 
            
    return dicionario_t, lista_id
    
def cria_lista_s1(permuta, dicionario_t):
    lista_agendamento_s1 = []
    tempo_chegada = 1
    for p in permuta:
        d = dicionario_t[p]
        for dados in d:
            lista_agendamento_s1.append((tempo_chegada, dados.id, dados.operacao, dados.atributo))
            tempo_chegada += 1

    return lista_agendamento_s1

def equivalencia_visao(lista_agendamento_s):
    dicionario_t, lista_id = separa_listas(lista_agendamento_s)
    lista_p = lista_permuta(lista_id)
    for permuta in lista_p:
        #print(dicionario_t[permuta[0]])
        print(permuta)
        lista_agendamento_s1 = cria_lista_s1(permuta,dicionario_t)
        print(lista_agendamento_s1)


