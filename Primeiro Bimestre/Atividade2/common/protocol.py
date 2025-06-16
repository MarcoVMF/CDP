from threading import Thread
import time
from common.utils import salvar_em_slave  # Função utilitária para salvar conteúdo no arquivo slave.txt


# Classe responsável por implementar os diferentes protocolos de sincronização com o servidor
class ProtocolHandler:
    def __init__(self, proxy, modo):
        """
        Inicializa o handler com a proxy de comunicação e o modo de protocolo desejado.
        :param proxy: Objeto RemoteProxy para comunicação com o servidor.
        :param modo: String representando o protocolo (R, RR, RRA).
        """
        self.proxy = proxy
        self.modo = modo.upper()  # Garante letras maiúsculas

    def sincronizar(self):
        """
        Executa o protocolo de sincronização selecionado.
        """
        if self.modo == "R":
            self._protocolo_R()
        elif self.modo == "RR":
            self._protocolo_RR()
        elif self.modo == "RRA":
            self._protocolo_RRA()
        else:
            print("Modo de protocolo inválido.")

    def _protocolo_R(self):
        """
        Protocolo R (Requisição Simples):
        Cliente apenas requisita e salva o conteúdo do arquivo.
        """
        print("[R] Solicitando conteúdo...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])  # Salva conteúdo em slave.txt
            print("Conteúdo salvo em slave.txt")
        else:
            print("Erro:", resp.get("error"))

    def _protocolo_RR(self):
        """
        Protocolo RR (Requisição + Confirmação):
        Cliente requisita o conteúdo e envia confirmação (ACK) após salvar.
        """
        print("[RR] Solicitando conteúdo com confirmação...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo. Enviando confirmação...")
            confirm = self.proxy.call("confirm_receipt", file="master.txt")  # Confirma que recebeu
            print("Confirmação enviada:", confirm)
        else:
            print("Erro:", resp.get("error"))

    def _protocolo_RRA(self):
        """
        Protocolo RRA (Requisição + ACK Assíncrono):
        Cliente requisita e salva o conteúdo, e envia o ACK de forma assíncrona após 5 segundos.
        """
        print("[RRA] Solicitando conteúdo com ACK assíncrono...")
        resp = self.proxy.call("get_file_content", file="master.txt")
        if "result" in resp:
            salvar_em_slave(resp["result"])
            print("Conteúdo salvo em slave.txt")
            print("Enviaremos o ACK em 5 segundos...")

            # Função que será executada em uma nova thread após um atraso
            def enviar_ack():
                time.sleep(5)
                ack = self.proxy.call("confirm_receipt", file="master.txt")
                print("\n ACK assíncrono enviado:", ack)

            # Dispara a thread para enviar o ACK sem bloquear a aplicação
            Thread(target=enviar_ack).start()
        else:
            print("Erro:", resp.get("error"))
