class Transacao():
    def __init__(self,transacao):
        self.tempo_chegada = int(transacao[0])
        self.id = int(transacao[1])
        self.operacao = transacao[2]
        self.atributo = transacao[3].split('\n')[0]
    
    def get_id(self):
        return self.id

    def get_operacao(self):
        return self.operacao    

    def get_atributo(self):
        return self.atributo

    def get_tempo_chegada(self):
        return self.tempo_chegada

