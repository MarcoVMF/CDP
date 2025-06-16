from datetime import datetime

LOG_PATH = "server/sync.log"

# Função responsável pela atualização do log
def log_sync(user, ip, status):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{datetime.now()} - {ip} - {user} - {status}\n")
