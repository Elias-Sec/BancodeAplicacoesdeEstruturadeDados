from modelos.ordem_servico import OrdemServico

class ManutencaoPreventiva(OrdemServico):
    def calcular_custo(self) -> float:
        return self.tempo_estimado * 2.00