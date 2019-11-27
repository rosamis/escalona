class Transacao():
    def __init__(self,transacao):
        self.tempo_chegada = int(transacao[0])
        self.id = int(transacao[1])
        self.operacao = transacao[2].upper()
        self.atributo = transacao[3].split('\n')[0].upper()

