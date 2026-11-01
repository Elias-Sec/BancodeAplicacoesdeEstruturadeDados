class Equipamento:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome

    def getNome(self) -> str:
        return self.nome