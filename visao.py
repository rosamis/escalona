import itertools

def lista_permuta(dicionario_t):
    lista_chave = []

    for chave in dicionario_t:
        lista_chave.append(chave)
    return list(itertools.permutations(lista_chave))

def separa_listas(lista_agendamento_s):
    lista_id = []
    dicionario_t = {}
    for s in lista_agendamento_s:
        if s.id not in lista_id:
            lista_id.append(s.id)
            x = [t for t in lista_agendamento_s if t.id == s.id]
            dicionario_t.update({s.id:x})
 
    return dicionario_t
    
def equivalencia_visao(lista_agendamento_s):
    dicionario_t = separa_listas(lista_agendamento_s)
    lista_p = lista_permuta(dicionario_t)
    print(dicionario_t)
    for permuta in lista_p:
        lista_agendamento_s1 = []
        print(dicionario_t[permuta[0]])
        

