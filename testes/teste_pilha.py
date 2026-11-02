# importa o sys pra mexer no caminho onde o Python procura os módulos
import sys
# importa o Path pra descobrir a pasta do projeto
from pathlib import Path

# coloca a pasta do projeto no caminho do Python, pra achar modelos, estruturas e servicos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# importa o equipamento que cada ordem de serviço usa
from modelos.equipamento import Equipamento
# importa a operação e a pilha que estão sendo testadas
from estruturas.pilha_historico import Operacao, PilhaHistorico
# importa o sistema, que usa a pilha pra desfazer alterações
from servicos.sistema_manutencao import SistemaManutencao


# mostra o estado da pilha do sistema com um título
def mostrar(sistema, rotulo):
    # imprime o título do momento
    print(rotulo)
    # imprime a pilha do topo até a base
    print("  pilha:", sistema.historico)
    # imprime quantas operações tem na pilha
    print("  tamanho da pilha:", sistema.historico.tamanho())
    # imprime uma linha em branco pra separar
    print()


# só executa os testes quando o arquivo é rodado direto
if __name__ == "__main__":
    # título do primeiro teste
    print("Teste 1 - pilha sozinha (LIFO)")
    # cria uma pilha nova e vazia
    gaveta = PilhaHistorico()
    # confere que ela começa vazia
    print("Vazia no inicio:", gaveta.esta_vazia())
    # consultar o topo de pilha vazia devolve None
    print("Topo da pilha vazia:", gaveta.consultar_topo())
    # cria a primeira operação: ordem 101 saindo de Pendente
    primeira = Operacao(101, "Pendente", "Em execução")
    # cria a segunda operação: ordem 101 indo pra Concluída
    segunda = Operacao(101, "Em execução", "Concluída")
    # empilha a primeira (vai ficar embaixo)
    gaveta.empilhar(primeira)
    # empilha a segunda (vai ficar no topo)
    gaveta.empilhar(segunda)
    # mostra qual operação está no topo
    print("Topo:", gaveta.consultar_topo())
    # o topo tem que ser a última que entrou
    assert gaveta.consultar_topo() is segunda
    # a primeira a sair tem que ser a última que entrou (LIFO)
    assert gaveta.desempilhar() is segunda
    # a segunda a sair é a que entrou primeiro
    assert gaveta.desempilhar() is primeira
    # depois de tirar tudo a pilha tem que estar vazia
    assert gaveta.esta_vazia()
    # tenta tirar de uma pilha vazia pra ver o aviso
    try:
        # isso deve dar erro porque não tem nada na pilha
        gaveta.desempilhar()
        # se chegou aqui, o erro não aconteceu e o teste está errado
        print("ERRO: desempilhou pilha vazia")
    # captura o aviso de pilha vazia
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Pilha vazia avisou certo:", erro)
    # linha em branco pra separar os testes
    print()

    # título do segundo teste
    print("Teste 2 - cenario obrigatorio da OS101")
    # cria um sistema novo com tudo vazio
    sistema = SistemaManutencao()
    # cria o equipamento da ordem
    transformador = Equipamento(1, "Transformador da subestacao")
    # cadastra a OS101, que nasce Pendente
    sistema.cadastrar_ordem("preventiva", 101, transformador, "Revisao geral", 3, 40)
    # pega a ordem 101 pra poder conferir o status dela
    ordem = sistema.consultar_ordem(101)
    # mostra o status inicial
    print("Status inicial:", ordem.status)
    # a OS101 tem que começar Pendente
    assert ordem.status == "Pendente"

    # o técnico altera para Em execução
    sistema.iniciar_execucao(101)
    # o técnico altera para Concluída
    sistema.concluir_ordem(101)
    # mostra a pilha com as duas alterações
    mostrar(sistema, "Depois de iniciar e concluir:")
    # a ordem tem que estar Concluída
    assert ordem.status == "Concluída"
    # a pilha tem que ter 2 operações
    assert sistema.historico.tamanho() == 2

    # o operador executa o primeiro desfazer
    sistema.desfazer()
    # mostra a pilha depois do primeiro desfazer
    mostrar(sistema, "Primeiro desfazer:")
    # a ordem tem que voltar pra Em execução
    assert ordem.status == "Em execução"
    # a pilha tem que ter só 1 operação (desfazer não cria operação nova)
    assert sistema.historico.tamanho() == 1

    # o operador executa o segundo desfazer
    sistema.desfazer()
    # mostra a pilha depois do segundo desfazer
    mostrar(sistema, "Segundo desfazer:")
    # a ordem tem que voltar pra Pendente
    assert ordem.status == "Pendente"
    # a pilha tem que estar vazia
    assert sistema.historico.esta_vazia()

    # tenta desfazer sem ter histórico
    try:
        # isso deve dar erro porque a pilha está vazia
        sistema.desfazer()
        # se chegou aqui, o erro não aconteceu e o teste está errado
        print("ERRO: desfez sem ter historico")
    # captura o aviso de histórico vazio
    except ValueError as erro:
        # imprime a mensagem do aviso
        print("Desfazer sem historico avisou certo:", erro)
    # linha em branco pra separar os testes
    print()

    # título do terceiro teste
    print("Teste 3 - tres ordens, alterando e desfazendo")
    # cria um sistema novo com tudo vazio
    sistema = SistemaManutencao()
    # cria o equipamento da OS101
    religador = Equipamento(2, "Religador Norte")
    # cria o equipamento da OS102
    painel = Equipamento(3, "Painel de comando")
    # cria o equipamento da OS103
    gerador = Equipamento(4, "Gerador de emergencia")
    # cadastra a OS101 (preventiva)
    sistema.cadastrar_ordem("preventiva", 101, religador, "Troca de isolador", 4, 30)
    # cadastra a OS102 (corretiva)
    sistema.cadastrar_ordem("corretiva", 102, painel, "Disjuntor desarmando", 1, 60)
    # cadastra a OS103 (preventiva)
    sistema.cadastrar_ordem("preventiva", 103, gerador, "Teste de partida", 3, 15)
    # guarda a OS101 numa variável pra conferir depois
    os101 = sistema.consultar_ordem(101)
    # guarda a OS102 numa variável pra conferir depois
    os102 = sistema.consultar_ordem(102)
    # guarda a OS103 numa variável pra conferir depois
    os103 = sistema.consultar_ordem(103)

    # coloca a OS101 em execução
    sistema.iniciar_execucao(101)
    # coloca a OS102 em execução
    sistema.iniciar_execucao(102)
    # mostra os status das duas
    print("101 e 102 em execucao:", os101.status, "|", os102.status)
    # guarda o tamanho da pilha antes de desfazer
    tamanho_antes = sistema.historico.tamanho()
    # desfaz a última alteração (a da OS102)
    sistema.desfazer()
    # a OS102 tem que voltar pra Pendente
    assert os102.status == "Pendente"
    # a pilha tem que ter encolhido 1, sem operação nova
    assert sistema.historico.tamanho() == tamanho_antes - 1
    # mostra o status da OS102 depois do desfazer
    print("Desfez a 102:", os102.status)

    # conclui a OS101
    sistema.concluir_ordem(101)
    # coloca a OS103 em execução
    sistema.iniciar_execucao(103)
    # mostra a pilha com as três alterações
    mostrar(sistema, "101 concluida e 103 em execucao:")
    # a OS101 tem que estar Concluída
    assert os101.status == "Concluída"
    # a OS103 tem que estar Em execução
    assert os103.status == "Em execução"

    # desfaz a última alteração (a da OS103)
    sistema.desfazer()
    # a OS103 tem que voltar pra Pendente
    assert os103.status == "Pendente"
    # mostra o status da OS103 depois do desfazer
    print("Desfez a 103:", os103.status)

    # desfaz a conclusão da OS101
    sistema.desfazer()
    # a OS101 tem que voltar pra Em execução
    assert os101.status == "Em execução"
    # mostra o status da OS101 depois do desfazer
    print("Desfez a conclusao da 101:", os101.status)

    # coloca a OS102 em execução de novo
    sistema.iniciar_execucao(102)
    # conclui a OS102
    sistema.concluir_ordem(102)
    # a OS102 tem que estar Concluída
    assert os102.status == "Concluída"
    # mostra a pilha nesse momento
    mostrar(sistema, "102 iniciada e concluida:")

    # desfaz a conclusão da OS102
    sistema.desfazer()
    # a OS102 tem que voltar pra Em execução
    assert os102.status == "Em execução"
    # desfaz o início da OS102
    sistema.desfazer()
    # a OS102 tem que voltar pra Pendente
    assert os102.status == "Pendente"
    # desfaz o início da OS101
    sistema.desfazer()
    # a OS101 tem que voltar pra Pendente
    assert os101.status == "Pendente"
    # mostra a pilha depois de desfazer tudo
    mostrar(sistema, "Tudo desfeito:")
    # a pilha tem que estar vazia
    assert sistema.historico.esta_vazia()
    # as três ordens têm que estar Pendentes como no começo
    assert os101.status == os102.status == os103.status == "Pendente"

    # avisa que chegou no fim sem nenhum erro
    print("Todos os testes da pilha passaram.")
