import grafo

def lista_escalona(lista_transacoes):
    """
    Lista que guarda listas com os escalonamentos
    """
    lista_commit = [t for t in lista_transacoes if t.operacao == 'C']
    transacoes_atuais = []
    lista_escalona = []
    lista_aux =  []
    for transacao in lista_transacoes:
        #print("-------------------------------------------")
        #print("transacao atual = ", transacao)
        #print("transacoes_atuais = ", transacoes_atuais)
        # print(lista_commit)
        #print("Lista AUX = ", lista_aux)
        if transacao.id not in transacoes_atuais:
            transacoes_atuais.append(transacao.id)
        if transacao in lista_commit:
            transacoes_atuais.remove(transacao.id)
        lista_aux.append(transacao)
        if len(transacoes_atuais) == 0:
            lista_escalona.append(lista_aux)
            lista_aux = []

    return lista_escalona
        
def gera_saida(grafo,id_escalonamento):
    if grafo.verificar_ciclos(grafo.vertices[0]):
        return (id_escalonamento,grafo.vertices,'NS')
    else:
        return (id_escalonamento,grafo.vertices,'SS')
     

def serializacao_conflito(lista_transacoes):
    lista_escalonados = lista_escalona(lista_transacoes)
    lista_saidas = []
    id_escalonamento = 1
    for escalonamento in lista_escalonados:
        lista_passados = []
        g = grafo.Grafo("serial")
        for tj in escalonamento:
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
        lista_saidas.append(gera_saida(g,id_escalonamento))
        id_escalonamento += 1

    return lista_saidas