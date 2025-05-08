from datetime import datetime

def read_file_content(filename):
    with open(filename, 'r') as f:
        return f.read()
    


def log_sync_event(status, ip, username, details=""):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{now}] {status} | IP: {ip} | Usuário: {username} | {details}\n"

    with open("sync.log", "a") as log_file:
        log_file.write(log_line)