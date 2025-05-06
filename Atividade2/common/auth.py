SLAVE_FILE = "slave.txt"

def salvar_em_slave(conteudo):
    with open(SLAVE_FILE, "w") as f:
        f.write(conteudo)

def carregar_slave():
    try:
        with open(SLAVE_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""