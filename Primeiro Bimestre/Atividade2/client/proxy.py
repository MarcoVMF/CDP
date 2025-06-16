# Importa módulos para requisições HTTP e manipulação de URLs e JSON
import urllib.request
import urllib.parse
import json

# Classe RemoteProxy: atua como intermediária entre o cliente e o servidor remoto
class RemoteProxy:
    def __init__(self, server_url, username, password):
        # Armazena a URL do servidor e as credenciais de autenticação
        self.url = server_url
        self.username = username
        self.password = password

    # Método genérico para fazer chamadas ao servidor
    def call(self, action, **params):
        # Monta os parâmetros da URL, incluindo usuário, senha e quaisquer parâmetros adicionais
        query_params = {
            "user": self.username,
            "pass": self.password,
            **params  # Desempacota os parâmetros fornecidos na chamada
        }
        # Codifica os parâmetros para o formato de query string
        query_string = urllib.parse.urlencode(query_params)

        # Constrói a URL completa da requisição
        full_url = f"{self.url}/{action}?{query_string}"

        try:
            # Realiza a requisição GET ao servidor
            with urllib.request.urlopen(full_url) as response:
                raw_data = response.read().decode()  # Lê e decodifica a resposta
                return json.loads(raw_data)  # Converte o JSON retornado em um dicionário
        except urllib.error.HTTPError as e:
            # Captura erros HTTP, como 404 ou 500
            return {"error": f"Erro HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            # Captura erros de conexão (ex: servidor fora do ar)
            return {"error": f"Erro de conexão: {e.reason}"}
        except json.JSONDecodeError:
            # Captura erros de formatação da resposta (caso não seja JSON válido)
            return {"error": "Resposta inválida do servidor (não é JSON)"}
