from abc import ABC, abstractmethod
from modelos.equipamento import Equipamento


class OrdemServico(ABC):

    def __init__(
        self,
        id: int,
        equipamento: Equipamento,
        descricao: str,
        prioridade: int,
        tempo_estimado: int
    ):
        if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
            raise ValueError("O ID deve ser um inteiro positivo.")

        if not isinstance(equipamento, Equipamento):
            raise TypeError("O equipamento deve ser um objeto Equipamento.")

        if not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("A descrição não pode ser vazia.")

        if (
            not isinstance(tempo_estimado, int)
            or isinstance(tempo_estimado, bool)
            or tempo_estimado <= 0
        ):
            raise ValueError("O tempo estimado deve ser um inteiro positivo.")

        self.id = id
        self.equipamento = equipamento
        self.descricao = descricao
        self.prioridade = prioridade
        self.tempo_estimado = tempo_estimado
        self.status = "Pendente"

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, p: int):
        if not isinstance(p, int) or isinstance(p, bool) or not 1 <= p <= 5:
            raise ValueError("A prioridade deve ser um inteiro entre 1 e 5.")

        self._prioridade = p

    def setPrioridade(self, p: int):
        self.prioridade = p

    def iniciarExecucao(self):
        if self.status != "Pendente":
            raise ValueError("A ordem de serviço não está pendente.")

        self.status = "Em execução"

    def concluir(self):
        if self.status != "Em execução":
            raise ValueError(
                "A ordem precisa estar em execução para ser concluída."
            )

        self.status = "Concluída"

    @abstractmethod
    def calcular_custo(self) -> float:
        pass