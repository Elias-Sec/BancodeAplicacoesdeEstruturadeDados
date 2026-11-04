from servicos.sistema_manutencao import SistemaManutencao
from modelos.equipamento import Equipamento

def main():
    sistema = SistemaManutencao()
    
    while True:
        print("\n====== SISTEMA INDUSTRIAL ======")
        print("1 - Cadastrar ordem de serviço")
        print("2 - Adicionar ordem à fila")
        print("3 - Atender próxima ordem")
        print("4 - Concluir ordem")
        print("5 - Consultar ordem por ID")
        print("6 - Listar ordens cadastradas")
        print("7 - Desfazer última alteração")
        print("8 - Exibir fila de atendimento")
        print("9 - Exibir relatório operacional")
        print("0 - Encerrar")
        
        opcao = input("Escolha uma opção: ")
        
        try:
            if opcao == '1':
                tipo = input("Tipo (preventiva/corretiva): ")
                numero = int(input("Número (ID da Ordem): "))
                
                id_equip = int(input("ID do Equipamento: "))
                nome_equip = input("Nome do Equipamento: ")
                
                descricao = input("Descrição do serviço: ")
                prioridade = int(input("Prioridade (1 a 5): "))
                tempo_estimado = int(input("Tempo estimado (horas): "))
                
                equipamento = Equipamento(id_equip, nome_equip) 
                
                sistema.cadastrar_ordem(tipo, numero, equipamento, descricao, prioridade, tempo_estimado)
                print(f"Ordem {numero} cadastrada com sucesso!")
                
            elif opcao == '2':
                numero = int(input("Número (ID) da Ordem a adicionar à fila: ")) # Convertido para int
                sistema.adicionar_a_fila(numero)
                print(f"Ordem {numero} adicionada à fila com sucesso!")
                
            elif opcao == '3':
                ordem = sistema.atender_proxima()
                print(f"Atendendo agora: OS{ordem.id} - {ordem.descricao}")
                
            elif opcao == '4':
                numero = int(input("Número (ID) da Ordem a concluir: ")) # Convertido para int
                sistema.concluir_ordem(numero)
                print(f"Ordem {numero} concluída com sucesso!")
                
            elif opcao == '5':
                numero = int(input("Número (ID) da Ordem: ")) # Convertido para int
                ordem = sistema.consultar_ordem(numero)
                print(f"OS{ordem.id} | Descrição: {ordem.descricao} | Status: {ordem.status}")
                
            elif opcao == '6':
                print("\n--- Lista de Ordens ---")
                sistema.listar_ordens()
                
            elif opcao == '7':
                operacao = sistema.desfazer()
                print(f"Desfeito com sucesso! Ordem {operacao.id_ordem} voltou para '{operacao.status_anterior}'.")
                
            elif opcao == '8':
                print("\n--- Fila de Atendimento ---")
                sistema.exibir_fila()
                
            elif opcao == '9':
                print("\n")
                sistema.relatorio()
                
            elif opcao == '0':
                print("Encerrando o sistema...")
                break
                
            elif opcao.upper() == 'C': 
                numero = int(input("Número (ID) da Ordem a cancelar: ")) # Convertido para int
                sistema.cancelar_ordem(numero)
                print(f"Ordem {numero} cancelada e removida das estruturas.")
                
            else:
                print("Opção inválida. Tente novamente.")
                
        except ValueError as erro:
            print(f"\n[!] ERRO NA OPERAÇÃO: {erro}")
        except TypeError as erro_tipo:
            print(f"\n[!] ERRO DE TIPO: {erro_tipo}")
        except Exception as e:
            print(f"\n[!] ERRO INESPERADO: {e}")

if __name__ == "__main__":
    main()