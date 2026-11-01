from modelos.ordem_servico import OrdemServico

class ManutencaoCorretiva(OrdemServico):
    def calcular_custo(self) -> float:
        return self.tempo_estimado * 3.50 + 150.00