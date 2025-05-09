from threading import Thread
import time
from common.utils import salvar_em_slave

# Definição da classe que controla a escolha e lógica dos protocolos
class ProtocolHandler:
    def __init__(self, proxy, modo):
        self.proxy = proxy
        self.modo = modo.upper()

    def sincronizar(self):
        if self.modo == "R":
            self._protocolo_R()
        elif self.modo == "RR":
            self._protocolo_RR()
        elif self.modo == "RRA":
            self._protocolo_RRA()
        else:
            print("Modo de protocolo inválido.")

    def _protocolo_R(self):
        print("[R] Solicitando conteúdo...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo em slave.txt")
        else:
            print("Erro:", resp.get("error"))

    def _protocolo_RR(self):
        print("[RR] Solicitando conteúdo com confirmação...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo. Enviando confirmação...")
            confirm = self.proxy.call("confirm_receipt", file="master.txt")
            print("Confirmação enviada:", confirm)
        else:
            print("Erro:", resp.get("error"))

    def _protocolo_RRA(self):
        print("[RRA] Solicitando conteúdo com ACK assíncrono...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo em slave.txt")
            print("Enviaremos o ACK em 5 segundos...")

            def enviar_ack():
                time.sleep(5)
                ack = self.proxy.call("confirm_receipt", file="master.txt")
                print("\n ACK assíncrono enviado:", ack)

            Thread(target=enviar_ack).start()
        else:
            print("Erro:", resp.get("error"))