import json
import hashlib

# Função para carregar o json dos usuários "cadastrados"
def load_users():
    with open('server/users.json') as f:
        return json.load(f)

# Função que efetivamente faz a autenticação dos usuários
def authenticate(username: str, password: str) -> bool:
    users = load_users()
    return users.get(username) == password
