#!/usr/bin/env python3
"""
Servidor de backup via sockets

Como executar:
python servidor_backup.py

- Recebe dados do monitor e grava em log-backup.log
- Escuta na porta 9000
"""
import socket
import threading

HOST = '0.0.0.0'
PORT = 9191
BACKUP_PATH = 'log-backup.log'

def handle_client(client_socket, addr):
    """Trata conexão de um cliente"""
    print(f"Cliente conectado: {addr}")
    try:
        # Recebe todos os dados do cliente
        data_buffer = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            data_buffer += chunk
        
        if data_buffer:
            # Decodifica e grava no arquivo de backup
            text = data_buffer.decode()
            with open(BACKUP_PATH, 'a', encoding='utf-8') as f:
                f.write(text)
            print(f"Dados recebidos e gravados: {len(text)} caracteres")
    
    except Exception as e:
        print(f"Erro ao processar cliente {addr}: {e}")
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f'Servidor de backup escutando em {HOST}:{PORT}...')
        
        try:
            while True:
                client, addr = server.accept()
                # Cria thread para cada cliente
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(client, addr)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServidor interrompido pelo usuário")

if __name__ == '__main__':
    main()