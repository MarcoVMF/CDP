from common.protocol import ProtocolHandler
from cliente.remote_proxy import RemoteFileProxy

def menu():
    print("\nProtocolos disponíveis:")
    print("1. R  (Requisição simples)")
    print("2. RR (Requisição + Confirmação)")
    print("3. RRA (Requisição + ACK assíncrono)")
    return input("Escolha o protocolo (1-3): ")

if __name__ == "__main__":
    url = "http://localhost:8000"
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    proxy = RemoteFileProxy(url, usuario, senha)
    handler = ProtocolHandler(proxy)

    opcao = menu()
    if opcao == "1":
        handler.protocolo_R()
    elif opcao == "2":
        handler.protocolo_RR()
    elif opcao == "3":
        handler.protocolo_RRA()
    else:
        print("Opção inválida.")
