import time
import hashlib

# Definição da classe responsável pelo monitoramento automático de modificações no master.txt
class SyncMonitor:
    def __init__(self, proxy, handler, interval: float = 5.0):
        self.proxy = proxy
        self.handler = handler
        self.interval = interval
        self.last_version = None

    def run(self):
        print("[MONITOR] Sincronização automática ativada.")
        while True:
            try:
                # Chama o método remoto que retorna a última modificação
                resp = self.proxy.call("check_master_version", file="master.txt")
                if "result" in resp:
                    version = resp["result"]
                    # Na primeira vez, ou se mudou, sincroniza
                    if self.last_version is None or version != self.last_version:
                        print("[MONITOR] Mudança detectada no master (versão: {}).".format(version))
                        self.handler.sincronizar()
                        self.last_version = version
                else:
                    # Caso haja erro no endpoint
                    print("[MONITOR ERRO] ", resp.get("error"))
                time.sleep(self.interval)

            except Exception as e:
                print(f"[ERRO] Monitoramento falhou: {e}")
                time.sleep(self.interval)