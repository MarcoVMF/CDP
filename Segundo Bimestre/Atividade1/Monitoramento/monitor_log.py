#!/usr/bin/env python3
"""
Monitoramento e backup via sockets

Como executar:
1. Primeiro execute: python servidor_backup.py
2. Em outro terminal: python monitor_log.py

- Monitora simula-log.log
- Envia novas linhas ao servidor de backup usando ThreadPoolExecutor
- Utiliza pool de até 3 threads para envio paralelo
"""
import os
import time
import socket
from concurrent.futures import ThreadPoolExecutor

# Caminho para o arquivo de log
LOG_PATH = 'simula-log.log'  # Caminho levando em conta que todos os .py estao na mesma pastas
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9191
MAX_THREADS = 3
POLL_INTERVAL = 1  # segundos

class MonitorLog:
    def __init__(self, path):
        self.path = path
        self._lines_sent = 0
        # Conta linhas iniciais se arquivo existir
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                self._lines_sent = len(f.readlines())
        else:
            print(f"Arquivo {self.path} não encontrado. Criando arquivo vazio...")
            with open(self.path, 'w', encoding='utf-8') as f:
                pass

    def tail(self):
        """Lê e retorna as linhas adicionadas desde a última verificação"""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new = lines[self._lines_sent:]
            self._lines_sent = len(lines)
            return new
        except FileNotFoundError:
            return []

    def send_chunk(self, chunk):
        """Envia um lote de linhas ao servidor via socket"""
        if not chunk:
            return
            
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)  # Timeout de 5 segundos
                sock.connect((SERVER_HOST, SERVER_PORT))
                
                # Envia todas as linhas do chunck
                data = ''.join(chunk)
                sock.sendall(data.encode('utf-8'))
                print(f"Enviado chunk com {len(chunk)} linhas")
                
        except ConnectionRefusedError:
            print('Erro: Servidor de backup não está rodando na porta', SERVER_PORT)
        except socket.timeout:
            print('Erro: Timeout na conexão com servidor')
        except Exception as e:
            print(f'Erro ao enviar dados: {e}')

    def run(self):
        """Loop principal de monitoramento"""
        print(f"Monitorando arquivo: {self.path}")
        print("Pressione Ctrl+C para parar")
        
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            try:
                while True:
                    time.sleep(POLL_INTERVAL)
                    new_lines = self.tail()
                    
                    if not new_lines:
                        continue
                    
                    print(f"Detectadas {len(new_lines)} novas linhas")
                    
                    # Divide novas linhas em chunks para as threads
                    chunk_size = max(1, len(new_lines) // MAX_THREADS)
                    chunks = [
                        new_lines[i:i+chunk_size] 
                        for i in range(0, len(new_lines), chunk_size)
                    ]
                    
                    # Envia cada chunk em uma thread separada
                    futures = []
                    for chunk in chunks:
                        future = executor.submit(self.send_chunk, chunk)
                        futures.append(future)
                    
                    # Aguarda conclusão de todos os envbios
                    for future in futures:
                        future.result()
                        
            except KeyboardInterrupt:
                print("\nMonitoramento interrompido pelo usuário")

if __name__ == '__main__':
    monitor = MonitorLog(LOG_PATH)
    print('Iniciando monitoramento de logs...')
    monitor.run()