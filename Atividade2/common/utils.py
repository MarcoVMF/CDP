import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client"))
SLAVE_FILE = os.path.join(BASE_DIR, "slave.txt")

# Definição dos métodos de atualização do slave.txt
def salvar_em_slave(conteudo):
    os.makedirs(BASE_DIR, exist_ok=True)  
    with open(SLAVE_FILE, "w") as f:
        f.write(conteudo)

# Definição do método que carrega para a memória o slave.txt
def carregar_slave():
    try:
        with open(SLAVE_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
