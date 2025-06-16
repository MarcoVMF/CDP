#!/usr/bin/env python3
"""
Análise paralela de padrões suspeitos

- Monitora log-backup.log
- Detecta dígitos repetidos (3 a 4) e envia alerta
"""
import os
import time
import re
import socket
from concurrent.futures import ThreadPoolExecutor

BACKUP_PATH   = 'log-backup.log'
ALERT_HOST    = '127.0.0.1'
ALERT_PORT    = 9100
MAX_THREADS   = 4
POLL_INTERVAL = 1

# Captura 2 a 4 dígitos idênticos em sequência
pattern = re.compile(r'(\d)\1{1,3}')

class AnaliseAmeacas:
    def __init__(self, path):
        self.path = path
        self._lines_read = 0
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self._lines_read = len(f.readlines())

    def tail(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        new = lines[self._lines_read:]
        self._lines_read = len(lines)
        return new

    def analyze(self, line):
        if pattern.search(line):
            parts = line.strip().split()
            user = parts[0] if parts else 'Unknown'
            ra   = parts[1] if len(parts) > 1 else 'N/A'
            msg  = f"{user} - {ra} - Possível Ameaça!"
            print(msg)
            # simula envio de alerta via socket
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((ALERT_HOST, ALERT_PORT))
                    sock.sendall(msg.encode())
            except ConnectionRefusedError:
                pass

    def run(self):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                time.sleep(POLL_INTERVAL)
                new_lines = self.tail()
                for line in new_lines:
                    executor.submit(self.analyze, line)

if __name__ == '__main__':
    print('Iniciando análise de ameaças...')
    AnaliseAmeacas(BACKUP_PATH).run()
