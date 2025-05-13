# Importa a classe RemoteProxy
from client.proxy import RemoteProxy

# Importa a classe SyncMonitor
from client.sync_monitor import SyncMonitor

# Importa a classe ProtocolHandler
from common.protocol import ProtocolHandler


# Função que exibe um menu de seleção de protocolos ao usuário
def menu_protocolo():
    print("\nProtocolos disponíveis:")
    print("1. R   (Requisição simples)")
    print("2. RR  (Requisição + Confirmação)")
    print("3. RRA (Requisição + ACK assíncrono)")
    
    # Lê a escolha do usuário
    escolha = input("Escolha o protocolo (1-3): ")

    # Retorna o protocolo correspondente à escolha
    if escolha == "1":
        return "R"
    elif escolha == "2":
        return "RR"
    elif escolha == "3":
        return "RRA"
    else:
        # Encerra o programa se a escolha for inválida
        print("Opção inválida.")
        exit(1)


# Bloco principal de execução
if __name__ == "__main__":
    # Define a URL do servidor remoto
    url = "http://localhost:8000"

    # Solicita as credenciais do usuário
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    # Executa o menu para seleção do protocolo de comunicação
    protocolo = menu_protocolo()

    # Cria o proxy remoto com a URL e credenciais fornecidas
    proxy = RemoteProxy(url, usuario, senha)

    # Cria o handler que executa o protocolo de sincronização escolhido
    handler = ProtocolHandler(proxy, protocolo)

    # Pergunta ao usuário se deseja ativar a sincronização automática
    escolha = input("Deseja ativar sincronização automática? (s/n): ").strip().lower()
    
    if escolha == "s":
        # Cria e inicia o monitor de sincronização automática
        monitor = SyncMonitor(proxy, handler)
        monitor.run()  # Executa o monitoramento periódico do arquivo mestre
    else:
        # Executa a sincronização manual sob demanda
        while True:
            input("\nPressione Enter para sincronizar manualmente...")
            handler.sincronizar()
