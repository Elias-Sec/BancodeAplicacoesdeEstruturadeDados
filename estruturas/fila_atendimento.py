from modelos.ordem_servico import OrdemServico


class Nodo:
    def __init__(self, dado: OrdemServico, proximo_nodo=None):
        self.dado = dado
        self.proximo_nodo = proximo_nodo

    def __repr__(self):
        return f"{self.dado!r} -> {self.proximo_nodo!r}"


class FilaAtendimento:
    def __init__(self):
        self.inicio: Nodo | None = None
        self.fim: Nodo | None = None
        self._tamanho = 0
        self._ids_objetos = set()

    def __repr__(self):
        return "[" + str(self.inicio) + "]"

    def enfileirar(self, ordem: OrdemServico):
        if not isinstance(ordem, OrdemServico):
            raise TypeError("A fila aceita apenas ordens de serviço.")

        if ordem.status == "Concluída":
            raise ValueError("Uma ordem concluída não pode entrar na fila.")

        identidade = id(ordem)

        if identidade in self._ids_objetos:
            raise ValueError("Esta ordem já está na fila.")

        novo_nodo = Nodo(ordem)

        if self.inicio is None:
            self.inicio = novo_nodo
            self.fim = novo_nodo
        else:
            if self.fim is not None:
                self.fim.proximo_nodo = novo_nodo
                self.fim = novo_nodo

        self._ids_objetos.add(identidade)
        self._tamanho += 1

    def desenfileirar(self):
        if self.inicio is None:
            return None

        nodo_removido = self.inicio
        ordem = nodo_removido.dado

        self.inicio = self.inicio.proximo_nodo

        if self.inicio is None:
            self.fim = None

        self._ids_objetos.remove(id(ordem))
        self._tamanho -= 1

        if ordem.status == "Pendente":
            ordem.iniciarExecucao()

        return ordem

    def consultar_proxima(self):
        if self.inicio is None:
            return None

        return self.inicio.dado

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho