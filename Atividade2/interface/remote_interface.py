from abc import ABC, abstractmethod

# Classe que define os métodos que o servidor disponibiliza remotamente
class RemoteInterface(ABC):
    @abstractmethod
    def get_file_content(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def check_master_version(self, username: str, password: str) -> float:
        pass

    @abstractmethod
    def log_sync_attempt(self, username: str, client_ip: str, status: str) -> None:
        pass