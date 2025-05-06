from common.utils import salvar_em_slave
import time
from threading import Thread

class ProtocolHandler:
    def __init__(self, proxy):
        self.proxy = proxy

    def protocolo_R(self):
        print("[R] Solicitando conteúdo...")
        resp = self.proxy.call("get_file_content", "master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo em slave.txt")
        else:
            print("Erro:", resp.get("error"))

    def protocolo_RR(self):
        print("[RR] Solicitando conteúdo com confirmação...")
        resp = self.proxy.call("get_file_content", "master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo. Enviando confirmação...")
            confirm = self.proxy.call("confirm_receipt", "master.txt")
            print("Confirmação enviada:", confirm)
        else:
            print("Erro:", resp.get("error"))

    def protocolo_RRA(self):
        print("[RRA] Solicitando conteúdo com ACK assíncrono...")
        resp = self.proxy.call("get_file_content", "master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo em slave.txt")
            print("Enviaremos o ACK em 5 segundos...")

            def enviar_ack():
                time.sleep(5)
                ack = self.proxy.call("confirm_receipt", "master.txt")
                print("ACK assíncrono enviado:", ack)

            Thread(target=enviar_ack).start()
        else:
            print("Erro:", resp.get("error"))