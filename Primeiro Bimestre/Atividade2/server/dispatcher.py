from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from server.file_handler import get_file_content, get_last_modified_time
from common.auth import authenticate
from server.logger import log_sync

# Classe que define o dispatcher HTTP — trata requisições GET vindas dos clientes
class Dispatcher(BaseHTTPRequestHandler):

    # Método que trata as requisições GET
    def do_GET(self):
        # Realiza o parsing da URL para extrair rota e parâmetros
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # Extrai usuário, senha e modo do protocolo (R, RR ou RRA), com valores padrão
        username = params.pop("user", [""])[0]
        password = params.pop("pass", [""])[0]
        mode     = params.pop("mode", ["R"])[0]
        action   = parsed.path.strip("/")  # Ação solicitada (por exemplo: get_file_content)

        client_ip = self.client_address[0]  # IP do cliente requisitante

        # Etapa de autenticação do usuário
        if not authenticate(username, password):
            self.send_response(403)  # Resposta HTTP: Proibido
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Authentication failed."}).encode())
            log_sync(username, client_ip, "FAIL_AUTH")  # Loga falha de autenticação
            return

        # Monta um dicionário com os parâmetros restantes (por exemplo, o nome do arquivo)
        extra_args = { k: v[0] for k, v in params.items() }

        try:
            # Busca o método correspondente à ação requisitada, prefixado com "remote_"
            method = getattr(self, f"remote_{action}")

            # Executa o método passando user, password e os parâmetros adicionais
            result = method(username, password, **extra_args)

            # Responde com sucesso e envia o resultado em formato JSON
            response = {"result": result}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            log_sync(username, client_ip, f"SUCCESS_{mode}")  # Loga sucesso

        except AttributeError:
            # Caso o método correspondente à ação não exista
            self.send_response(404)  # Recurso não encontrado
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Ação '{action}' não encontrada."}).encode())
            log_sync(username, client_ip, f"FAIL_NOACTION_{mode}")  # Loga erro de ação

        except Exception as e:
            # Trata qualquer outro erro inesperado
            self.send_response(500)  # Erro interno do servidor
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            log_sync(username, client_ip, "FAIL_INTERNAL")  # Loga falha interna

    # --- Métodos remotos expostos via HTTP ---

    def remote_get_file_content(self, user, pw, file):
        """
        Método remoto para retornar o conteúdo do arquivo master.txt.
        O nome do arquivo é ignorado propositalmente para segurança.
        """
        return get_file_content()

    def remote_check_master_version(self, user, pw, file):
        """
        Método remoto para retornar a versão (timestamp) da última modificação de master.txt.
        Usado para monitoramento de mudanças.
        """
        return str(get_last_modified_time())

    def remote_confirm_receipt(self, user, pw, file):
        """
        Método remoto para confirmar o recebimento do conteúdo pelo cliente.
        Apenas registra no log.
        """
        log_sync(user, self.client_address[0], "CONFIRM_RECEIPT")
        return "Recebimento confirmado"
