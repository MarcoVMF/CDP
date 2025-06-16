import threading

# Classe para definição das trheads para requisição feita ao servidor
class RequestThread(threading.Thread):
    def __init__(self, handler, *args, **kwargs):
        super().__init__()
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.handler(*self.args, **self.kwargs)
