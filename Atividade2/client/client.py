from client.proxy import RemoteProxy
from client.sync_monitor import SyncMonitor
from common.protocol import ProtocolHandler

# Definição do menu interativo do usuário
def menu_protocolo():
    print("\nProtocolos disponíveis:")
    print("1. R   (Requisição simples)")
    print("2. RR  (Requisição + Confirmação)")
    print("3. RRA (Requisição + ACK assíncrono)")
    escolha = input("Escolha o protocolo (1-3): ")
    if escolha == "1":
        return "R"
    elif escolha == "2":
        return "RR"
    elif escolha == "3":
        return "RRA"
    else:
        print("Opção inválida.")
        exit(1)

if __name__ == "__main__":
    url = "http://localhost:8000"
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    protocolo = menu_protocolo()
    proxy = RemoteProxy(url, usuario, senha)
    handler = ProtocolHandler(proxy, protocolo)

    escolha = input("Deseja ativar sincronização automática? (s/n): ").strip().lower()
    if escolha == "s":
        monitor = SyncMonitor(proxy, handler)
        monitor.run()  # Método que monitora periodicamente o arquivo master
    else:
        while True:
            input("\nPressione Enter para sincronizar manualmente...")
            handler.sincronizar()