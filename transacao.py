## @package transacao
#  Este arquivo contém a classe Transação.

## Classe que guarda uma transação.
#
class Transacao():
    ## Construtor da classe. Ele recebe uma string e atribui os valores correspondentes para cada atributo da classe.
    #
    #  @param self Ponteiro para o objeto.
    #  @param transacao É uma string.
    def __init__(self,transacao):
        ## Guarda um int que representa o tempo de chegada da transação.
        self.tempo_chegada = int(transacao[0])
        ## Guarda um int que representa o id da transação.
        self.id = int(transacao[1])
        ## Guarda uma string que representa a operação da transação. Pode ser R (read), W (write) ou C (commit).
        self.operacao = transacao[2].upper()
        ## Guarda uma string que representa o atributo da transação que sofrerá a operação.
        self.atributo = transacao[3].split('\n')[0].upper()

