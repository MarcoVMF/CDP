#!/usr/bin/env python3
"""
Análise paralela de padrões suspeitos

Como executar:
1. Certifique-se que log-backup.log existe
2. Execute: python analise_ameacas.py

- Monitora log-backup.log
- Detecta padrões suspeitos (sequências de 2 a 4 dígitos repetidos)
- Utiliza pool de até 4 threads para análise paralela
- Exemplos de padrões: 123333, 556677, 999999
"""
import os
import time
import re
import socket
from concurrent.futures import ThreadPoolExecutor

BACKUP_PATH   = 'log-backup.log'
ALERT_HOST    = '127.0.0.1'
ALERT_PORT    = 9190
MAX_THREADS   = 4
POLL_INTERVAL = 1

# Captura padrões como 123333 ou 556677 (sequênciaas de dígitos repetidos)
# Busca por 2-4 dígitos seguidos pela mesma sequência
pattern = re.compile(r'(\d{2,4})\1+|(\d)\2{3,}')

class AnaliseAmeacas:
    def __init__(self, path):
        self.path = path
        self._lines_read = 0
        
        # Cria arquivo se não existir
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                pass
        else:
            # Conta linhas já processadas
            with open(self.path, 'r', encoding='utf-8') as f:
                self._lines_read = len(f.readlines())

    def tail(self):
        """Lê novas linhas adicionadas ao arquivo"""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new = lines[self._lines_read:]
            self._lines_read = len(lines)
            return new
        except FileNotFoundError:
            return []

    def analyze(self, line):
        """Analisa uma linha em busca de padrões suspeitos"""
        match = pattern.search(line)
        if match:
            # Parse da linha no formato:
            # 2025-06-28 22:33:46 | User - 677635192 | Radius - a1:ab:3f:e8:2b:7d | Authenticate - 2025-06-28 22:33:56 | Device - Xiaomi
            
            try:
                parts = line.strip().split(' | ')
                if len(parts) >= 5:
                    timestamp = parts[0]
                    user_info = parts[1].replace('User - ', '')
                    radius_info = parts[2].replace('Radius - ', '')
                    auth_info = parts[3].replace('Authenticate - ', '')
                    device_info = parts[4].replace('Device - ', '')
                    
                    # Identifica o padrão encontrado
                    found_pattern = match.group()
                    
                    # Formato de saída solicitado
                    msg = f"{timestamp} | User - {user_info} | Radius - {radius_info} | Authenticate - {auth_info} | Device - {device_info} | AMEAÇA DETECTADA - Padrão: {found_pattern}"
                    print(f"🚨 ALERTA DE SEGURANÇA: {msg}")
                    
                    # Simula envio de alerta via socket (opcional)
                    self.send_alert(msg)
                else:
                    # Fallback para formato antigo
                    found_pattern = match.group()
                    msg = f"Linha suspeita detectada - Padrão: {found_pattern}"
                    print(f"🚨 {msg}")
                    self.send_alert(msg)
                    
            except Exception as e:
                # Em caso de erro no parsing, usa formato simples
                found_pattern = match.group()
                msg = f"Padrão suspeito detectado: {found_pattern}"
                print(f"🚨 {msg}")
                self.send_alert(msg)

    def send_alert(self, message):
        """Simula envio de alerta para servidor fictício"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.connect((ALERT_HOST, ALERT_PORT))
                sock.sendall(message.encode('utf-8'))
        except (ConnectionRefusedError, socket.timeout):
            pass
        except Exception as e:
            print(f"Erro ao enviar alerta: {e}")

    def run(self):
        """Loop principal de análise"""
        print(f"Analisando arquivo: {self.path}")
        print("Detectando padrões suspeitos (dígitos repetidos)...")
        print("Pressione Ctrl+C para parar")
        
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            try:
                while True:
                    time.sleep(POLL_INTERVAL)
                    new_lines = self.tail()
                    
                    if new_lines:
                        print(f"Analisando {len(new_lines)} novas linhas...")
                        
                        # Submete cada linha para análise em thread separada
                        futures = []
                        for line in new_lines:
                            future = executor.submit(self.analyze, line)
                            futures.append(future)
                        
                        # Aguarda conclusão de todas as análises
                        for future in futures:
                            future.result()
                            
            except KeyboardInterrupt:
                print("\nAnálise interrompida pelo usuário")

if __name__ == '__main__':
    print('Iniciando análise de ameaças...')
    analyzer = AnaliseAmeacas(BACKUP_PATH)
    analyzer.run()
