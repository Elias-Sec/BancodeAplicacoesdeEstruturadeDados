class No:
    def __init__(self, dado=None, proximo_nodo=None):
        self.dado = dado
        self.proximo_nodo = proximo_nodo

    def __repr__(self):
        return '%s -> %s' % (self.dado.id, self.proximo_nodo)


class ListaOrdens:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None
        self.quantidade = 0

    def __repr__(self):
        return "[" + str(self.primeiro) + "]"

    def buscar(self, id):
        passando = self.primeiro
        while passando is not None and passando.dado.id != id:
            passando = passando.proximo_nodo
        if passando is None:
            return None
        return passando.dado

    def inserir(self, ordem):
        if self.buscar(ordem.id) is not None:
            print("Ja existe uma ordem com o id", ordem.id)
            return False

        novo_no = No(ordem)

        if self.primeiro is None:
            self.primeiro = novo_no
            self.ultimo = novo_no
        else:
            self.ultimo.proximo_nodo = novo_no
            self.ultimo = novo_no

        self.quantidade = self.quantidade + 1
        return True

    def remover(self, id):
        if self.primeiro is None:
            print("A lista esta vazia")
            return None

        if self.primeiro.dado.id == id:
            tirada = self.primeiro.dado
            self.primeiro = self.primeiro.proximo_nodo
            if self.primeiro is None:
                self.ultimo = None
            self.quantidade = self.quantidade - 1
            return tirada

        atras = self.primeiro
        passando = self.primeiro.proximo_nodo
        while passando is not None and passando.dado.id != id:
            atras = passando
            passando = passando.proximo_nodo

        if passando is None:
            print("Ordem", id, "nao encontrada")
            return None

        atras.proximo_nodo = passando.proximo_nodo
        if passando == self.ultimo:
            self.ultimo = atras
        self.quantidade = self.quantidade - 1
        return passando.dado

    def atualizar_status(self, id, status):
        achada = self.buscar(id)
        if achada is None:
            print("Ordem", id, "nao encontrada")
            return False

        if status == "Em execução":
            achada.iniciarExecucao()
        elif status == "Concluída":
            achada.concluir()
        else:
            print("Status invalido pra essa operação:", status)
            return False
        return True

    def listar_pendentes(self):
        passando = self.primeiro
        teve = False
        while passando is not None:
            if passando.dado.status == "Pendente":
                print(passando.dado.id, "-", passando.dado.equipamento.nome, "-", passando.dado.descricao)
                teve = True
            passando = passando.proximo_nodo
        if not teve:
            print("Nenhuma ordem pendente.")

    def contar_por_prioridade(self, p):
        quantas = 0
        passando = self.primeiro
        while passando is not None:
            if passando.dado.prioridade == p:
                quantas = quantas + 1
            passando = passando.proximo_nodo
        return quantas
