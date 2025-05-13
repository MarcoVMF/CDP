# Importa a biblioteca time para controlar intervalos de execução
import time

# Classe responsável por monitorar automaticamente mudanças no arquivo master.txt do servidor
class SyncMonitor:
    def __init__(self, proxy, handler, interval: float = 5.0):
        """
        Inicializa o monitor de sincronização.
        :param proxy: Objeto RemoteProxy para comunicação com o servidor.
        :param handler: Objeto ProtocolHandler que executa a sincronização.
        :param interval: Intervalo de tempo (em segundos) entre cada verificação.
        """
        self.proxy = proxy                  # Comunicação com o servidor
        self.handler = handler              # Executa a lógica de sincronização
        self.interval = interval            # Intervalo entre verificações
        self.last_version = None            # Armazena a última versão conhecida do arquivo

    def run(self):
        """
        Inicia o processo de monitoramento em loop.
        Verifica periodicamente se houve alteração no arquivo master.txt do servidor.
        """
        print("[MONITOR] Sincronização automática ativada.")
        while True:
            try:
                # Chama o endpoint remoto que retorna a versão atual do master.txt
                resp = self.proxy.call("check_master_version", file="master.txt")

                if "result" in resp:
                    version = resp["result"]
                    
                    # Se é a primeira execução ou detectou alteração na versão do arquivo, sincroniza
                    if self.last_version is None or version != self.last_version:
                        print("[MONITOR] Mudança detectada no master (versão: {}).".format(version))
                        self.handler.sincronizar()  # Executa a sincronização via handler
                        self.last_version = version  # Atualiza a versão conhecida

                else:
                    # Exibe erro caso o servidor retorne falha
                    print("[MONITOR ERRO] ", resp.get("error"))

                # Aguarda o intervalo antes da próxima verificação
                time.sleep(self.interval)

            except Exception as e:
                # Captura erros inesperados durante o monitoramento
                print(f"[ERRO] Monitoramento falhou: {e}")
                time.sleep(self.interval)
