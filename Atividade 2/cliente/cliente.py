import sys
import time
from threading import Thread
from remote_proxy import RemoteFileProxy

SLAVE_FILE = "slave.txt"

def salvar_em_slave(conteudo):
    with open(SLAVE_FILE, "w") as f:
        f.write(conteudo)

def carregar_slave():
    try:
        with open(SLAVE_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def protocolo_R(proxy):
    print("[R] Solicitando conteúdo...")
    resp = proxy.call("get_file_content", "master.txt")
    if "result" in resp:
        salvar_em_slave(resp["result"])
        print("Conteúdo salvo em slave.txt")
    else:
        print("Erro:", resp.get("error"))

def protocolo_RR(proxy):
    print("[RR] Solicitando conteúdo com confirmação...")
    resp = proxy.call("get_file_content", "master.txt")
    if "result" in resp:
        salvar_em_slave(resp["result"])
        print("Conteúdo salvo. Enviando confirmação...")
        confirm = proxy.call("confirm_receipt", "master.txt")
        print("Confirmação enviada:", confirm)
    else:
        print("Erro:", resp.get("error"))

def protocolo_RRA(proxy):
    print("[RRA] Solicitando conteúdo com ACK assíncrono...")
    resp = proxy.call("get_file_content", "master.txt")
    if "result" in resp:
        salvar_em_slave(resp["result"])
        print("Conteúdo salvo em slave.txt")
        print("Enviaremos o ACK em 5 segundos...")

        def enviar_ack():
            time.sleep(5)
            ack = proxy.call("confirm_receipt", "master.txt")
            print("ACK assíncrono enviado:", ack)

        Thread(target=enviar_ack).start()
    else:
        print("Erro:", resp.get("error"))

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

    opcao = menu()
    if opcao == "1":
        protocolo_R(proxy)
    elif opcao == "2":
        protocolo_RR(proxy)
    elif opcao == "3":
        protocolo_RRA(proxy)
    else:
        print("Opção inválida.")
