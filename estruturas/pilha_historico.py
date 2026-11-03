# classe que representa um nodo (caixinha) da pilha encadeada
class Nodo:
    # construtor do nodo: guarda o dado e a ligação com o nodo de baixo
    def __init__(self, dado=None, proximo_nodo=None):
        # guarda a informação do nodo (aqui vai ser sempre uma Operacao)
        self.dado = dado
        # guarda o nodo que fica logo abaixo na pilha (None se for o último)
        self.proximo_nodo = proximo_nodo

    # define como o nodo aparece quando é impresso
    def __repr__(self):
        # mostra "dado -> proximo", e o próximo repete o mesmo até chegar no None
        return '%s -> %s' % (self.dado, self.proximo_nodo)


# classe que guarda UMA alteração de status feita numa ordem de serviço
class Operacao:
    # construtor: recebe o id da ordem, o status de antes e o status de depois
    def __init__(self, id_ordem, status_anterior, status_novo):
        # sem o id da ordem a operação não faz sentido, então barra aqui
        if id_ordem is None:
            # avisa o erro para quem tentou criar a operação sem id
            raise ValueError("A operacao precisa do id da ordem.")
        # guarda qual ordem foi alterada
        self.id_ordem = id_ordem
        # guarda o status que a ordem tinha antes (é pra onde o desfazer volta)
        self.status_anterior = status_anterior
        # guarda o status que a ordem passou a ter depois da alteração
        self.status_novo = status_novo

    # define como a operação aparece quando é impressa
    def __repr__(self):
        # mostra no formato "OS101 (Pendente -> Em execução)"
        return "OS%s (%s -> %s)" % (self.id_ordem, self.status_anterior, self.status_novo)


# pilha encadeada com política LIFO (o último que entra é o primeiro que sai)
class PilhaHistorico:
    # construtor: cria a pilha vazia
    def __init__(self):
        # o topo aponta pro último nodo empilhado (None = pilha vazia)
        self.topo = None
        # conta quantas operações estão na pilha
        self.quantidade = 0

    # define como a pilha aparece quando é impressa
    def __repr__(self):
        # mostra a pilha do topo até o fim, dentro de colchetes
        return "[" + str(self.topo) + "]"

    # coloca uma operação no topo da pilha
    def empilhar(self, operacao):
        # só aceita objetos do tipo Operacao, pra não guardar coisa errada
        if not isinstance(operacao, Operacao):
            # avisa o erro quando o tipo é outro
            raise TypeError("So da pra empilhar objeto do tipo Operacao.")
        # cria o nodo novo apontando pro antigo topo e ele vira o novo topo
        self.topo = Nodo(operacao, self.topo)
        # soma 1 na quantidade de operações
        self.quantidade = self.quantidade + 1

    # tira a operação do topo da pilha e devolve ela
    def desempilhar(self):
        # não dá pra tirar nada de uma pilha vazia
        if self.topo is None:
            # avisa que não existe operação pra desfazer
            raise ValueError("Nao tem nenhuma operacao pra desfazer.")
        # guarda o nodo do topo pra poder devolver o dado dele
        saindo = self.topo
        # o topo passa a ser o nodo que estava embaixo
        self.topo = saindo.proximo_nodo
        # solta o nodo que saiu, pra ele não ficar ligado na pilha
        saindo.proximo_nodo = None
        # tira 1 da quantidade de operações
        self.quantidade = self.quantidade - 1
        # devolve a operação que estava no topo
        return saindo.dado

    # olha a operação do topo sem tirar ela da pilha
    def consultar_topo(self):
        # se a pilha está vazia não tem topo pra consultar
        if self.topo is None:
            # devolve None quando está vazia
            return None
        # devolve a operação que está no topo
        return self.topo.dado

    # diz se a pilha está vazia
    def esta_vazia(self):
        # True quando não tem nenhum nodo no topo
        return self.topo is None

    # diz quantas operações existem na pilha
    def tamanho(self):
        # devolve o contador que é atualizado a cada empilhar e desempilhar
        return self.quantidade
