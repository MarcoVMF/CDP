from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from server.file_handler import get_file_content, get_last_modified_time
from common.auth import authenticate
from server.logger import log_sync

# Classe que define o funcionamento do dispatcher, que faz o intermédio da comunicação entre servidor e cliente
class Dispatcher(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        username = params.pop("user", [""])[0]
        password = params.pop("pass", [""])[0]
        mode     = params.pop("mode", ["R"])[0]
        action   = parsed.path.strip("/")

        client_ip = self.client_address[0]

        # Autenticação
        if not authenticate(username, password):
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Authentication failed."}).encode())
            log_sync(username, client_ip, "FAIL_AUTH")
            return

        # Constrói dict de outros parâmetros (ex: file)
        extra_args = { k: v[0] for k, v in params.items() }

        try:
            method = getattr(self, f"remote_{action}")
            # Passa username, password e quaisquer args extras
            result = method(username, password, **extra_args)

            response = {"result": result}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            log_sync(username, client_ip, f"SUCCESS_{mode}")

        except AttributeError:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Ação '{action}' não encontrada."}).encode())
            log_sync(username, client_ip, f"FAIL_NOACTION_{mode}")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            log_sync(username, client_ip, "FAIL_INTERNAL")

    def remote_get_file_content(self, user, pw, file):
        # Ignora o nome do arquivo fixo; sempre recupera master.txt
        return get_file_content()

    def remote_check_master_version(self, user, pw, file):
        return str(get_last_modified_time())

    def remote_confirm_receipt(self, user, pw, file):
        # Marca no log que o cliente confirmou a recepção
        log_sync(user, self.client_address[0], "CONFIRM_RECEIPT")
        return "Recebimento confirmado"
