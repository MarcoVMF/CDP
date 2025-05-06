from http.server import BaseHTTPRequestHandler
import json
import os

class RemoteDispatcher(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        method = data['method']
        args = data.get('args', [])

        # Autenticação (7)
        auth_header = self.headers.get("Authorization")
        if not self.server.authenticate(auth_header):
            self.send_error(403, "Forbidden")
            return

        try:
            # (3) Esqueleto Dinâmico com getattr
            func = getattr(self.server.remote_object, method)
            result = func(*args)
            response = {"result": result}
        except Exception as e:
            response = {"error": str(e)}

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

class RemoteObject:
    def get_file_content(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def check_master_version(self):
        return "v1.0"
    
    def confirm_receipt(self, filename):
        print(f"[Confirmação recebida] Cliente confirmou recebimento de '{filename}'")
        return "Confirmação registrada com sucesso."

