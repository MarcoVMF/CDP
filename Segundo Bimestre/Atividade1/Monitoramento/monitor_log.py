"""
Monitoramento e backup via sockets

- Monitora simula-log.log
- Envia novas linhas ao servidor de backup usando ThreadPoolExecutor
"""
import os
import time
import socket
from concurrent.futures import ThreadPoolExecutor

## LOG_PATH = '/home/221255265/Monitoramento/simula-log.log'
LOG_PATH = 'simula-log.log'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9000
MAX_THREADS = 3
POLL_INTERVAL = 1  # segundos

class MonitorLog:
    def __init__(self, path):
        self.path = path
        self._lines_sent = 0
        # conta linhas iniciais
        with open(self.path, 'r') as f:
            self._lines_sent = len(f.readlines())

    def tail(self):
        """Lê e retorna as linhas adicionadas"""
        with open(self.path, 'r') as f:
            lines = f.readlines()
        new = lines[self._lines_sent:]
        self._lines_sent = len(lines)
        return new

    def send_chunk(self, chunk):
        """Envia um lote de linhas ao servidor via socket"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SERVER_HOST, SERVER_PORT))
                for line in chunk:
                    sock.sendall(line.encode())
        except ConnectionRefusedError:
            print('Conexão recusada: servidor de backup não está rodando')

    def run(self):
        """Loop principal de monitoramento"""
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                time.sleep(POLL_INTERVAL)
                new_lines = self.tail()
                if not new_lines:
                    continue
                # divide novas linhas em partes para as threads
                chunk_size = max(1, len(new_lines) // MAX_THREADS)
                chunks = [new_lines[i:i+chunk_size] for i in range(0, len(new_lines), chunk_size)]
                for chunk in chunks:
                    executor.submit(self.send_chunk, chunk)

if __name__ == '__main__':
    monitor = MonitorLog(LOG_PATH)
    print('Iniciando monitoramento de logs...')
    monitor.run()