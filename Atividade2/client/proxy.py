import urllib.request
import urllib.request
import urllib.parse
import json

# Definição da proxy, que funciona como intermediário entre a comunicação do cliente e servidor


# Proxy entre cliente e servidor
class RemoteProxy:
    def __init__(self, server_url, username, password):
        self.url = server_url
        self.username = username
        self.password = password

    def call(self, action, **params):
        # Monta os parâmetros da URL com autenticação
        query_params = {
            "user": self.username,
            "pass": self.password,
            **params
        }
        query_string = urllib.parse.urlencode(query_params)
        full_url = f"{self.url}/{action}?{query_string}"

        try:
            with urllib.request.urlopen(full_url) as response:
                raw_data = response.read().decode()
                return json.loads(raw_data)  # Espera que o servidor retorne JSON
        except urllib.error.HTTPError as e:
            return {"error": f"Erro HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"error": f"Erro de conexão: {e.reason}"}
        except json.JSONDecodeError:
            return {"error": "Resposta inválida do servidor (não é JSON)"}
