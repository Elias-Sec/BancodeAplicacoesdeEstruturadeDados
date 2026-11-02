# importa o sys pra mexer no caminho onde o Python procura os módulos
import sys
# importa o Path pra descobrir a pasta do projeto
from pathlib import Path

# coloca a pasta do projeto no caminho do Python, pra achar modelos, estruturas e servicos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# importa o equipamento que cada ordem de serviço usa
from modelos.equipamento import Equipamento
# importa o sistema que está sendo testado
from servicos.sistema_manutencao import SistemaManutencao


# só executa os testes quando o arquivo é rodado direto
if __name__ == "__main__":
    # cria o sistema com cadastro, fila e histórico vazios
    sistema = SistemaManutencao()
    # cria o equipamento da primeira ordem
    religador = Equipamento(1, "Religador Norte")
    # cria o equipamento da segunda ordem
    painel = Equipamento(2, "Painel de comando")
    # cria o equipamento da terceira ordem
    gerador = Equipamento(3, "Gerador de emergencia")

    # cadastra a OS201 (preventiva)
    sistema.cadastrar_ordem("preventiva", 201, religador, "Troca de isolador", 4, 30)
    # cadastra a OS202 (corretiva)
    sistema.cadastrar_ordem("corretiva", 202, painel, "Disjuntor desarmando", 1, 60)
    # cadastra a OS203 (corretiva)
    sistema.cadastrar_ordem("corretiva", 203, gerador, "Nao da partida", 2, 45)
    # título da listagem
    print("Cadastro:")
    # imprime as três ordens cadastradas
    sistema.listar_ordens()
    # linha em branco pra separar
    print()

    # tenta cadastrar um id que já existe
    try:
        # isso deve dar erro de id repetido
        sistema.cadastrar_ordem("preventiva", 201, religador, "Repetida", 2, 10)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: aceitou id repetido")
    # captura o aviso de id repetido
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (id repetido):", erro)
    # tenta cadastrar um tipo que não existe
    try:
        # isso deve dar erro de tipo inválido
        sistema.cadastrar_ordem("outro", 204, religador, "Teste", 2, 10)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: aceitou tipo invalido")
    # captura o aviso de tipo inválido
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (tipo errado):", erro)
    # tenta consultar uma ordem que não existe
    try:
        # isso deve dar erro de ordem não encontrada
        sistema.consultar_ordem(999)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: achou ordem que nao existe")
    # captura o aviso de ordem não encontrada
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (ordem que nao existe):", erro)
    # linha em branco pra separar
    print()

    # coloca a OS201 na fila
    sistema.adicionar_a_fila(201)
    # coloca a OS202 na fila
    sistema.adicionar_a_fila(202)
    # coloca a OS203 na fila
    sistema.adicionar_a_fila(203)
    # tenta colocar a OS202 na fila de novo
    try:
        # isso deve dar erro de ordem repetida na fila
        sistema.adicionar_a_fila(202)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: aceitou ordem repetida na fila")
    # captura o aviso de ordem repetida
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (ordem repetida na fila):", erro)
    # tenta iniciar direto uma ordem que está na fila
    try:
        # isso deve dar erro porque a ordem tem que sair pelo atendimento
        sistema.iniciar_execucao(201)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: iniciou ordem que estava na fila")
    # captura o aviso de ordem na fila
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (iniciar ordem que esta na fila):", erro)
    # título da fila
    print("Fila:")
    # imprime as ordens esperando na fila
    sistema.exibir_fila()
    # linha em branco pra separar
    print()

    # atende a primeira da fila
    atendida = sistema.atender_proxima()
    # mostra qual ordem foi atendida e o status dela
    print("Atendida: OS%s -> %s" % (atendida.id, atendida.status))
    # a primeira da fila era a OS201
    assert atendida.id == 201
    # a fila tem que ter ficado com 2 ordens
    assert sistema.fila.tamanho() == 2
    # linha em branco pra separar
    print()

    # conclui a OS201, que está em execução
    sistema.concluir_ordem(201)
    # tenta concluir uma ordem que ainda está pendente
    try:
        # isso deve dar erro porque a OS203 não está em execução
        sistema.concluir_ordem(203)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: concluiu ordem pendente")
    # captura o aviso de transição inválida
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (concluir ordem pendente):", erro)
    # linha em branco pra separar
    print()

    # cancela a OS202, que está pendente no meio da fila
    cancelada = sistema.cancelar_ordem(202)
    # mostra qual ordem foi cancelada
    print("Cancelada: OS%s" % cancelada.id)
    # tenta consultar a ordem cancelada
    try:
        # isso deve dar erro porque ela saiu do cadastro
        sistema.consultar_ordem(202)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: a ordem cancelada ainda existe")
    # captura o aviso de ordem não encontrada
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (consultar a cancelada):", erro)
    # tenta cancelar uma ordem que já foi concluída
    try:
        # isso deve dar erro porque só pendente pode ser cancelada
        sistema.cancelar_ordem(201)
        # se chegou aqui, o erro não aconteceu
        print("ERRO: cancelou ordem concluida")
    # captura o aviso de cancelamento não permitido
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Falhou como esperado (cancelar ordem concluida):", erro)
    # a fila tem que ter sobrado só com a OS203
    assert sistema.fila.tamanho() == 1
    # a próxima da fila tem que ser a OS203
    assert sistema.fila.consultar_proxima().id == 203
    # título da fila depois do cancelamento
    print("Fila depois do cancelamento:")
    # imprime a fila
    sistema.exibir_fila()
    # linha em branco pra separar
    print()

    # desfaz a conclusão da OS201
    sistema.desfazer()
    # a OS201 tem que voltar pra Em execução
    assert sistema.consultar_ordem(201).status == "Em execução"
    # desfaz o atendimento da OS201
    sistema.desfazer()
    # a OS201 tem que voltar pra Pendente
    assert sistema.consultar_ordem(201).status == "Pendente"
    # mostra o status final da OS201
    print("Desfez conclusao e atendimento da 201:", sistema.consultar_ordem(201).status)
    # o histórico tem que estar vazio
    assert sistema.historico.esta_vazia()
    # linha em branco pra separar
    print()

    # imprime o relatório final do sistema
    sistema.relatorio()
