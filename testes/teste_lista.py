import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.equipamento import Equipamento
from modelos.manutencao_preventiva import ManutencaoPreventiva
from modelos.manutencao_corretiva import ManutencaoCorretiva
from estruturas.lista_ligada import ListaOrdens


def mostrar_ponteiros(cadastro):
    print("Lista:", cadastro)
    if cadastro.primeiro is None:
        print("primeiro: None | ultimo: None | quantidade:", cadastro.quantidade)
    else:
        print("primeiro:", cadastro.primeiro.dado.id, "| ultimo:", cadastro.ultimo.dado.id, "| quantidade:", cadastro.quantidade)
    print()


if __name__ == "__main__":
    religador = Equipamento(1, "Religador Norte")
    capacitores = Equipamento(2, "Banco de capacitores")
    seccionadora = Equipamento(3, "Chave seccionadora")
    painel = Equipamento(4, "Painel de comando")
    para_raios = Equipamento(5, "Para-raios da linha 7")
    gerador = Equipamento(6, "Gerador de emergencia")

    cadastro = ListaOrdens()

    print("Cadastrando 5 ordens")
    cadastro.inserir(ManutencaoPreventiva(1, religador, "Troca de isolador", 4, 30))
    cadastro.inserir(ManutencaoCorretiva(2, capacitores, "Capacitor estufado", 2, 45))
    cadastro.inserir(ManutencaoPreventiva(3, seccionadora, "Lubrificar contatos", 4, 20))
    cadastro.inserir(ManutencaoCorretiva(4, painel, "Disjuntor desarmando sozinho", 1, 60))
    cadastro.inserir(ManutencaoCorretiva(5, para_raios, "Para-raios trincado", 5, 90))
    mostrar_ponteiros(cadastro)

    print("Removendo a primeira (id 1)")
    cadastro.remover(1)
    mostrar_ponteiros(cadastro)

    print("Removendo a ultima (id 5)")
    cadastro.remover(5)
    mostrar_ponteiros(cadastro)

    print("Inserindo uma nova (id 6)")
    cadastro.inserir(ManutencaoPreventiva(6, gerador, "Teste de partida", 3, 15))
    mostrar_ponteiros(cadastro)

    print("Removendo do meio (id 3)")
    cadastro.remover(3)
    mostrar_ponteiros(cadastro)

    print("Tentando inserir id repetido (2)")
    cadastro.inserir(ManutencaoPreventiva(2, painel, "Repetida", 2, 10))
    print()

    print("Tentando remover id que nao existe (99)")
    cadastro.remover(99)
    print()

    print("Buscar id 4:", cadastro.buscar(4).descricao)
    print("Buscar id 99:", cadastro.buscar(99))
    print()

    print("Colocando a ordem 2 em execução")
    cadastro.atualizar_status(2, "Em execução")
    print("Status da 2:", cadastro.buscar(2).status)
    print()

    print("Ordens pendentes:")
    cadastro.listar_pendentes()
    print()

    print("Quantas com prioridade 2:", cadastro.contar_por_prioridade(2))
    print("Quantas com prioridade 5:", cadastro.contar_por_prioridade(5))
