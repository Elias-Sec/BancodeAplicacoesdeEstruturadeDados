import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.equipamento import Equipamento
from modelos.manutencao_preventiva import ManutencaoPreventiva
from modelos.manutencao_corretiva import ManutencaoCorretiva
from estruturas.fila_atendimento import FilaAtendimento


def exibir_estado(fila):
    """Exibe o estado atual da fila."""
    print(f"Fila: {fila}")
    print(f"Tamanho: {fila.tamanho()}")
    print(f"Está vazia? {'Sim' if fila.esta_vazia() else 'Não'}")

    proxima = fila.consultar_proxima()

    if proxima is not None:
        print(f"Próxima ordem: {proxima.id} - {proxima.descricao}")
        print(f"Status da próxima ordem: {proxima.status}")
    else:
        print("Próxima ordem: nenhuma")

    print("-" * 55)


def testar_fila_atendimento():
    fila = FilaAtendimento()

    equipamento1 = Equipamento(1, "Motor industrial")
    equipamento2 = Equipamento(2, "Esteira transportadora")
    equipamento3 = Equipamento(3, "Compressor")

    ordem1 = ManutencaoPreventiva(
        1, equipamento1, "Inspecao do motor", 2, 3
    )

    ordem2 = ManutencaoCorretiva(
        2, equipamento2, "Reparo da esteira", 1, 5
    )

    ordem3 = ManutencaoPreventiva(
        3, equipamento3, "Revisao do compressor", 3, 2
    )

    print("\n" + "=" * 55)
    print("TESTE 1 — ESTADO INICIAL DA FILA")
    print("=" * 55)

    assert fila.esta_vazia() is True
    assert fila.tamanho() == 0
    assert fila.consultar_proxima() is None

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 2 — INSERÇÃO DA PRIMEIRA ORDEM")
    print("=" * 55)

    fila.enfileirar(ordem1)

    assert fila.esta_vazia() is False
    assert fila.tamanho() == 1
    assert fila.consultar_proxima() is ordem1

    print(f"Adicionada: Ordem {ordem1.id} - {ordem1.descricao}")
    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 3 — INSERÇÃO DE OUTRAS ORDENS")
    print("=" * 55)

    fila.enfileirar(ordem2)
    print(f"Adicionada: Ordem {ordem2.id} - {ordem2.descricao}")

    fila.enfileirar(ordem3)
    print(f"Adicionada: Ordem {ordem3.id} - {ordem3.descricao}")

    assert fila.tamanho() == 3
    assert fila.consultar_proxima() is ordem1

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 4 — TENTATIVA DE INSERIR ORDEM DUPLICADA")
    print("=" * 55)

    try:
        fila.enfileirar(ordem1)
        assert False, "A fila aceitou uma ordem duplicada."
    except ValueError as erro:
        print(f"Erro esperado: {erro}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO — duplicata rejeitada\n")

    print("=" * 55)
    print("TESTE 5 — REMOÇÃO DA PRIMEIRA ORDEM")
    print("=" * 55)

    removida = fila.desenfileirar()

    assert removida is not None
    assert removida is ordem1
    assert removida.status == "Em execução"
    assert fila.tamanho() == 2
    assert fila.consultar_proxima() is ordem2

    print(f"Ordem removida: {removida.id} - {removida.descricao}")
    print(f"Novo status: {removida.status}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 6 — REMOÇÃO DA SEGUNDA ORDEM")
    print("=" * 55)

    removida = fila.desenfileirar()

    assert removida is not None
    assert removida is ordem2
    assert removida.status == "Em execução"
    assert fila.tamanho() == 1
    assert fila.consultar_proxima() is ordem3

    print(f"Ordem removida: {removida.id} - {removida.descricao}")
    print(f"Novo status: {removida.status}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 7 — REMOÇÃO DA ÚLTIMA ORDEM")
    print("=" * 55)

    removida = fila.desenfileirar()

    assert removida is not None
    assert removida is ordem3
    assert removida.status == "Em execução"
    assert fila.tamanho() == 0
    assert fila.esta_vazia() is True
    assert fila.consultar_proxima() is None

    print(f"Ordem removida: {removida.id} - {removida.descricao}")
    print(f"Novo status: {removida.status}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 8 — TENTATIVA DE REMOVER DE UMA FILA VAZIA")
    print("=" * 55)

    removida = fila.desenfileirar()

    assert removida is None
    assert fila.tamanho() == 0

    print(f"Retorno da remoção: {removida}")
    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TESTE 9 — TENTATIVA DE INSERIR ORDEM CONCLUÍDA")
    print("=" * 55)

    ordem4 = ManutencaoCorretiva(
        4, equipamento1, "Troca de componente", 4, 2
    )

    ordem4.iniciarExecucao()
    ordem4.concluir()

    print(f"Ordem criada: {ordem4.id} - {ordem4.descricao}")
    print(f"Status antes da inserção: {ordem4.status}")

    try:
        fila.enfileirar(ordem4)
        assert False, "A fila aceitou uma ordem concluída."
    except ValueError as erro:
        print(f"Erro esperado: {erro}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO — ordem concluída rejeitada\n")

    print("=" * 55)
    print("TESTE 10 — REINSERÇÃO DE ORDEM REMOVIDA")
    print("=" * 55)

    fila.enfileirar(ordem1)

    assert fila.tamanho() == 1
    assert fila.consultar_proxima() is ordem1

    print(f"Ordem reinserida: {ordem1.id} - {ordem1.descricao}")
    print(f"Status atual: {ordem1.status}")

    exibir_estado(fila)
    print("RESULTADO: APROVADO\n")

    print("=" * 55)
    print("TODOS OS TESTES FORAM CONCLUÍDOS COM SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    testar_fila_atendimento()