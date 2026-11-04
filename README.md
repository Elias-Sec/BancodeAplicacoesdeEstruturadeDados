# BancodeAplicacoesdeEstruturadeDados
# Sistema Industrial de Manutenção 

Este projeto é uma aplicação de linha de comando desenvolvida em Python para o gerenciamento de Ordens de Serviço (OS) em um ambiente industrial. O sistema integra conceitos de Programação Orientada a Objetos (POO) e **Estruturas de Dados Dinâmicas** construídas do zero.

##  Estruturas de Dados Utilizadas

Para garantir o controle rigoroso da memória e do fluxo de execução, o projeto implementa suas próprias estruturas encadeadas:

*   **Lista Ligada (`ListaOrdens`)**: Gerencia o cadastro principal de todas as ordens de serviço (Preventivas e Corretivas).
*   **Fila Dinâmica (`FilaAtendimento`)**: Organiza as ordens que aguardam atendimento, respeitando a ordem de chegada (FIFO).
*   **Pilha (`PilhaHistorico`)**: Armazena o histórico de operações (mudanças de status), permitindo a funcionalidade de "Desfazer" a última ação (LIFO).

##  Funcionalidades e Requisitos Acadêmicos

O sistema possui um menu interativo (CLI) para cadastro, enfileiramento, atendimento, conclusão e geração de relatórios operacionais, atendendo a requisitos específicos de integração e consistência:

*   **Validação Rigorosa (Questão 5):** O sistema integra as estruturas impedindo operações inválidas (ex: enfileirar uma ordem já concluída ou criar OS com tipagem incorreta) e mantém a consistência total entre o cadastro, a fila e o histórico.
*   **Operação Atômica de Cancelamento (Questão 6):** Implementação de uma operação de cancelamento de OS Pendentes. A operação garante integridade referencial: caso ocorra falha durante a remoção, o estado anterior é preservado. 
    *   *Complexidade Temporal:* **O(N)**, pois exige a varredura linear da Lista Ligada e da Fila Dinâmica para localizar a ordem, seguida da religação dos ponteiros dos nós, que ocorre em *O(1)*.

##  Como Executar o Projeto

Certifique-se de ter o Python 3.x instalado em sua máquina. O projeto foi estruturado em módulos para facilitar a manutenção.

1. Abra o terminal na **pasta raiz** do projeto.
2. Execute o arquivo principal:

python main.py

GRUPO: Lucas, Rafael, Rodrigo e Wendell.