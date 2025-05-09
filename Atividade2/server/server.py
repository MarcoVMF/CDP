# server_main.py
from http.server import HTTPServer
from server.dispatcher import Dispatcher
import threading

def run_server():
    server = HTTPServer(("localhost", 8000), Dispatcher)
    print("[INFO] Servidor rodando em http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
