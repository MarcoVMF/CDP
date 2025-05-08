import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../cliente"))
SLAVE_FILE = os.path.join(BASE_DIR, "slave.txt")

def salvar_em_slave(conteudo):
    os.makedirs(BASE_DIR, exist_ok=True)  
    with open(SLAVE_FILE, "w") as f:
        f.write(conteudo)

def carregar_slave():
    try:
        with open(SLAVE_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
