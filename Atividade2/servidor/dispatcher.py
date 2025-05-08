from http.server import BaseHTTPRequestHandler
from interface.remote_interface import RemoteFileInterface
from servidor.file_handler import log_sync_event, read_file_content
from base64 import b64decode
import json


class RemoteDispatcher(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        method = data['method']
        args = data.get('args', [])

        auth_header = self.headers.get("Authorization")
        client_ip = self.client_address[0]

        try:
            _, encoded = auth_header.split(" ")
            decoded = b64decode(encoded).decode()
            username, _ = decoded.split(":")
        except:
            username = "DESCONHECIDO"

        if not self.server.authenticate(auth_header):
            log_sync_event("FALHA", client_ip, username, f"Tentativa de autenticação mal-sucedida no método {method}")
            self.send_error(403, "Forbidden")
            return

        log_sync_event("TENTATIVA", client_ip, username, f"Método: {method}, Args: {args}")

        try:
            func = getattr(self.server.remote_object, method)
            result = func(*args)
            response = {"result": result}
            log_sync_event("SUCESSO", client_ip, username, f"Método executado: {method}")
        except Exception as e:
            response = {"error": str(e)}
            log_sync_event("FALHA", client_ip, username, f"Erro ao executar '{method}': {e}")
        finally:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())


class RemoteObject(RemoteFileInterface):
    def get_file_content(self, filename):
        return read_file_content(filename)

    def check_master_version(self):
        return "v1.0"
    
    def confirm_receipt(self, filename):
        print(f"[Confirmação recebida] Cliente confirmou recebimento de '{filename}'")
        return "Confirmação registrada com sucesso."