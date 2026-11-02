# importa a classe de manutenção preventiva
from modelos.manutencao_preventiva import ManutencaoPreventiva
# importa a classe de manutenção corretiva
from modelos.manutencao_corretiva import ManutencaoCorretiva
# importa a lista ligada que guarda o cadastro das ordens
from estruturas.lista_ligada import ListaOrdens
# importa a fila que guarda as ordens esperando atendimento
from estruturas.fila_atendimento import FilaAtendimento
# importa a operação e a pilha que guardam o histórico de alterações
from estruturas.pilha_historico import Operacao, PilhaHistorico

# texto do status de uma ordem que ainda não começou (igual ao da OrdemServico)
PENDENTE = "Pendente"
# texto do status de uma ordem que está sendo executada
EM_EXECUCAO = "Em execução"
# texto do status de uma ordem que já terminou
CONCLUIDA = "Concluída"


# classe que junta o cadastro (lista), o atendimento (fila) e o histórico (pilha)
class SistemaManutencao:
    # tabela que liga o texto do tipo à classe que deve ser criada
    TIPOS = {
        # tipo preventiva cria um objeto ManutencaoPreventiva
        "preventiva": ManutencaoPreventiva,
        # tipo corretiva cria um objeto ManutencaoCorretiva
        "corretiva": ManutencaoCorretiva,
    }

    # construtor: cria o sistema com as três estruturas vazias
    def __init__(self):
        # lista ligada com todas as ordens cadastradas
        self.cadastro = ListaOrdens()
        # fila com as ordens que esperam um técnico
        self.fila = FilaAtendimento()
        # pilha com as alterações de status que podem ser desfeitas
        self.historico = PilhaHistorico()

    # cadastra uma ordem nova (preventiva ou corretiva) e devolve ela
    def cadastrar_ordem(self, tipo, numero, equipamento, descricao, prioridade, tempo_estimado):
        # tira espaços e deixa minúsculo pra comparar com a tabela de tipos
        chave = str(tipo).strip().lower()
        # se o tipo não está na tabela, não dá pra criar a ordem
        if chave not in self.TIPOS:
            # avisa que o tipo é inválido
            raise ValueError("Tipo invalido, use preventiva ou corretiva.")
        # não pode existir outra ordem com o mesmo id
        if self.cadastro.buscar(numero) is not None:
            # avisa que o id já está em uso
            raise ValueError("Ja existe uma ordem com o id %s." % numero)
        # pega a classe certa na tabela (preventiva ou corretiva)
        classe = self.TIPOS[chave]
        # cria o objeto da ordem (o construtor valida os dados)
        nova = classe(numero, equipamento, descricao, prioridade, tempo_estimado)
        # coloca a ordem no final da lista de cadastro
        self.cadastro.inserir(nova)
        # devolve a ordem criada
        return nova

    # procura uma ordem pelo id e devolve ela
    def consultar_ordem(self, numero):
        # usa o método auxiliar que já avisa se a ordem não existe
        return self._obter(numero)

    # imprime todas as ordens cadastradas
    def listar_ordens(self):
        # começa pelo primeiro nodo da lista
        andando = self.cadastro.primeiro
        # se não tem nodo nenhum, o cadastro está vazio
        if andando is None:
            # avisa que não tem ordem
            print("Nenhuma ordem cadastrada.")
        # percorre a lista até acabar os nodos
        while andando is not None:
            # pega a ordem que está guardada no nodo
            ordem = andando.dado
            # imprime id, equipamento, descrição, prioridade e status da ordem
            print("OS%s | %s | %s | prioridade %s | %s" % (
                ordem.id, ordem.equipamento.nome, ordem.descricao, ordem.prioridade, ordem.status))
            # anda para o próximo nodo da lista
            andando = andando.proximo_nodo

    # coloca uma ordem já cadastrada no final da fila de atendimento
    def adicionar_a_fila(self, numero):
        # busca a ordem no cadastro (dá erro se não existir)
        ordem = self._obter(numero)
        # só ordem pendente pode esperar na fila
        if ordem.status != PENDENTE:
            # avisa que o status não permite entrar na fila
            raise ValueError("So ordem pendente entra na fila.")
        # não pode colocar a mesma ordem duas vezes na fila
        if self._na_fila(ordem):
            # avisa que a ordem já está esperando
            raise ValueError("A ordem %s ja esta na fila." % numero)
        # coloca a ordem no final da fila
        self.fila.enfileirar(ordem)
        # devolve a ordem que entrou na fila
        return ordem

    # imprime as ordens que estão na fila, da primeira até a última
    def exibir_fila(self):
        # começa pelo primeiro nodo da fila
        andando = self.fila.inicio
        # se não tem nodo, a fila está vazia
        if andando is None:
            # avisa que a fila está vazia
            print("A fila esta vazia.")
        # posição da ordem na fila, começando em 1
        posicao = 1
        # percorre a fila até acabar os nodos
        while andando is not None:
            # pega a ordem que está guardada no nodo
            ordem = andando.dado
            # imprime a posição, o id, a descrição e a prioridade
            print("%s - OS%s | %s | prioridade %s" % (posicao, ordem.id, ordem.descricao, ordem.prioridade))
            # anda para o próximo nodo da fila
            andando = andando.proximo_nodo
            # soma 1 na posição pra próxima ordem
            posicao = posicao + 1

    # atende a primeira ordem da fila e registra a alteração no histórico
    def atender_proxima(self):
        # se a fila está vazia não tem quem atender
        if self.fila.esta_vazia():
            # avisa que não tem ordem esperando
            raise ValueError("Nao tem ordem esperando na fila.")
        # guarda o status de antes, que vai pro histórico
        anterior = self.fila.consultar_proxima().status
        # tira a primeira da fila (a fila já muda o status pra Em execução)
        ordem = self.fila.desenfileirar()
        # guarda no histórico a mudança de status do atendimento
        self.historico.empilhar(Operacao(ordem.id, anterior, ordem.status))
        # devolve a ordem que foi atendida
        return ordem

    # muda o status de uma ordem e registra a alteração no histórico
    def alterar_status(self, numero, novo_status):
        # busca a ordem no cadastro (dá erro se não existir)
        ordem = self._obter(numero)
        # ordem que está na fila só pode começar pelo atendimento (respeita a ordem da fila)
        if novo_status == EM_EXECUCAO and self._na_fila(ordem):
            # avisa que precisa usar o atender próxima
            raise ValueError("A ordem %s esta na fila, use atender proxima." % numero)
        # guarda o status de antes, que vai pro histórico
        anterior = ordem.status
        # pede pra lista mudar o status (a ordem confere se a mudança é permitida)
        deu_certo = self.cadastro.atualizar_status(numero, novo_status)
        # se a lista não conseguiu mudar, não registra nada no histórico
        if not deu_certo:
            # avisa que a mudança não foi feita
            raise ValueError("Nao foi possivel mudar a ordem %s." % numero)
        # guarda no histórico a mudança que deu certo
        self.historico.empilhar(Operacao(ordem.id, anterior, ordem.status))
        # devolve a ordem já alterada
        return ordem

    # passa a ordem de Pendente para Em execução
    def iniciar_execucao(self, numero):
        # usa o alterar_status, que também registra no histórico
        return self.alterar_status(numero, EM_EXECUCAO)

    # passa a ordem de Em execução para Concluída
    def concluir_ordem(self, numero):
        # usa o alterar_status, que também registra no histórico
        return self.alterar_status(numero, CONCLUIDA)

    # desfaz a última alteração de status, sem criar operação nova na pilha
    def desfazer(self):
        # sem histórico não tem o que desfazer
        if self.historico.esta_vazia():
            # avisa que a pilha está vazia
            raise ValueError("Nao tem alteracao pra desfazer.")
        # olha a última operação sem tirar da pilha ainda
        operacao = self.historico.consultar_topo()
        # procura no cadastro a ordem que foi alterada
        ordem = self.cadastro.buscar(operacao.id_ordem)
        # se a ordem não existe mais, não dá pra voltar o status
        if ordem is None:
            # avisa que a ordem sumiu do cadastro
            raise ValueError("A ordem %s nao esta mais no cadastro." % operacao.id_ordem)
        # o status atual precisa ser o mesmo que a operação guardou como novo
        if ordem.status != operacao.status_novo:
            # avisa que o histórico não bate com a ordem
            raise ValueError("Historico fora de sincronia com a ordem %s." % ordem.id)
        # volta o status direto na ordem, sem passar pelo alterar_status (por isso não empilha nada)
        ordem.status = operacao.status_anterior
        # só agora tira a operação do topo, depois que tudo deu certo
        self.historico.desempilhar()
        # devolve a operação desfeita pra quem chamou mostrar na tela
        return operacao

    # cancela uma ordem pendente, tirando ela da fila e do cadastro
    def cancelar_ordem(self, numero):
        # busca a ordem no cadastro (dá erro se não existir)
        ordem = self._obter(numero)
        # só dá pra cancelar ordem que ainda não começou
        if ordem.status != PENDENTE:
            # avisa que o status não permite cancelar
            raise ValueError("So da pra cancelar ordem pendente.")
        # se a ordem está esperando na fila, tira ela de lá primeiro
        if self._na_fila(ordem):
            # remove o nodo da ordem de dentro da fila
            self._tirar_da_fila(ordem)
        # remove a ordem do cadastro
        self.cadastro.remover(numero)
        # devolve a ordem cancelada
        return ordem

    # imprime o relatório com contagem por status e custos
    def relatorio(self):
        # contador de ordens pendentes
        pendentes = 0
        # contador de ordens em execução
        em_execucao = 0
        # contador de ordens concluídas
        concluidas = 0
        # soma dos custos das preventivas
        custo_preventivas = 0.0
        # soma dos custos das corretivas
        custo_corretivas = 0.0
        # começa pelo primeiro nodo do cadastro
        andando = self.cadastro.primeiro
        # percorre o cadastro inteiro
        while andando is not None:
            # pega a ordem que está guardada no nodo
            ordem = andando.dado
            # conta a ordem no grupo do status dela
            if ordem.status == PENDENTE:
                # soma 1 nas pendentes
                pendentes = pendentes + 1
            # se não é pendente, confere se está em execução
            elif ordem.status == EM_EXECUCAO:
                # soma 1 nas em execução
                em_execucao = em_execucao + 1
            # o que sobrou é concluída
            else:
                # soma 1 nas concluídas
                concluidas = concluidas + 1
            # separa o custo pelo tipo da ordem
            if isinstance(ordem, ManutencaoCorretiva):
                # soma o custo calculado pela corretiva
                custo_corretivas = custo_corretivas + ordem.calcular_custo()
            # se não é corretiva, é preventiva
            else:
                # soma o custo calculado pela preventiva
                custo_preventivas = custo_preventivas + ordem.calcular_custo()
            # anda para o próximo nodo do cadastro
            andando = andando.proximo_nodo

        # imprime o título do relatório
        print("------ RELATORIO ------")
        # imprime o total de ordens cadastradas
        print("Ordens cadastradas:", self.cadastro.quantidade)
        # imprime quantas estão pendentes
        print("Pendentes:", pendentes)
        # imprime quantas estão em execução
        print("Em execução:", em_execucao)
        # imprime quantas estão concluídas
        print("Concluídas:", concluidas)
        # imprime quantas estão esperando na fila
        print("Na fila:", self.fila.tamanho())
        # imprime quantas alterações ainda podem ser desfeitas
        print("Alteracoes que podem ser desfeitas:", self.historico.tamanho())
        # imprime o custo das preventivas em reais
        print("Custo preventivas: R$ %.2f" % custo_preventivas)
        # imprime o custo das corretivas em reais
        print("Custo corretivas: R$ %.2f" % custo_corretivas)
        # imprime o custo total em reais
        print("Custo total: R$ %.2f" % (custo_preventivas + custo_corretivas))

    # busca a ordem no cadastro e avisa se ela não existe
    def _obter(self, numero):
        # procura a ordem pelo id na lista
        ordem = self.cadastro.buscar(numero)
        # se a busca não achou nada, a ordem não existe
        if ordem is None:
            # avisa que a ordem não foi encontrada
            raise ValueError("Ordem %s nao encontrada." % numero)
        # devolve a ordem encontrada
        return ordem

    # confere se a ordem está esperando na fila
    def _na_fila(self, ordem):
        # começa pelo primeiro nodo da fila
        andando = self.fila.inicio
        # percorre a fila até acabar os nodos
        while andando is not None:
            # compara se o nodo guarda exatamente essa ordem
            if andando.dado is ordem:
                # achou a ordem na fila
                return True
            # anda para o próximo nodo da fila
            andando = andando.proximo_nodo
        # chegou no fim e não achou
        return False

    # tira uma ordem de qualquer posição da fila (a fila não tem método pra isso)
    def _tirar_da_fila(self, ordem):
        # guarda o nodo de trás, que vai precisar ser religado
        atras = None
        # começa pelo primeiro nodo da fila
        andando = self.fila.inicio
        # anda até achar o nodo da ordem ou acabar a fila
        while andando is not None and andando.dado is not ordem:
            # guarda o nodo atual como o de trás
            atras = andando
            # anda para o próximo nodo
            andando = andando.proximo_nodo
        # se chegou no fim, a ordem não estava na fila
        if andando is None:
            # avisa que não removeu nada
            return False
        # se não tem nodo de trás, a ordem era a primeira da fila
        if atras is None:
            # o início da fila passa a ser o segundo nodo
            self.fila.inicio = andando.proximo_nodo
        # senão a ordem estava no meio ou no final
        else:
            # o nodo de trás pula o nodo removido
            atras.proximo_nodo = andando.proximo_nodo
        # se o nodo removido era o último, o fim da fila volta um nodo
        if andando is self.fila.fim:
            # o fim da fila passa a ser o nodo de trás
            self.fila.fim = atras
        # tira a ordem do controle de ordens repetidas da fila
        self.fila._ids_objetos.remove(id(ordem))
        # tira 1 do tamanho da fila
        self.fila._tamanho = self.fila._tamanho - 1
        # avisa que removeu com sucesso
        return True
