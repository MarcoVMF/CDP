import os

MASTER_PATH = "server/master.txt"

# Função para fazer a leitura do arquivo
def get_file_content() -> str:
    with open(MASTER_PATH, 'r') as f:
        return f.read()

# Função para identificar o timestamp da última modificação
def get_last_modified_time() -> float:
    return os.path.getmtime(MASTER_PATH)
