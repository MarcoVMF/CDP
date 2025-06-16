#!/usr/bin/env python3
"""
Servidor de backup via sockets

- Recebe dados do monitor e grava em log-backup.log
"""
import socket

HOST = '0.0.0.0'
PORT = 9000
BACKUP_PATH = 'log-backup.log'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f'Servidor de backup escutando em {HOST}:{PORT}...')
    while True:
        client, addr = server.accept()
        with client:
            data = client.recv(4096)
            if not data:
                continue
            
            # processa primeiro bloco de dados
            text = data.decode()
            if not text.endswith('\n'):
                text += '\n'
            
            # grava no arquivo de backup
            with open(BACKUP_PATH, 'a') as f:
                f.write(text)
            
            # continua lendo se houver mais dados
            while True:
                data = client.recv(4096)
                if not data:
                    break
                
                text = data.decode()
                if not text.endswith('\n'):
                    text += '\n'
                    
                with open(BACKUP_PATH, 'a') as f:
                    f.write(text)