from http.server import HTTPServer
from dispatcher import RemoteDispatcher, RemoteObject
from threading import Thread
from base64 import b64decode
import json

def load_users():
    with open("users.json", "r") as file:
        data = json.load(file)

    return data['users']


class AuthenticatedServer(HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        self.remote_object = RemoteObject()

    def authenticate(self, auth_header):
        if not auth_header:
            return False
        try:
            method, encoded = auth_header.split(" ")
            userpass = b64decode(encoded).decode()
            user, passwd = userpass.split(":")
            data = load_users()
            for user_json in data:
                if user_json['username'] == user:
                    if user_json['password'] == passwd:
                        return True
            return False

        except:
            return False

if __name__ == '__main__':

    def run_server():
        server = AuthenticatedServer(("localhost", 8000), RemoteDispatcher)
        print("Servidor ativo em http://localhost:8000")
        server.serve_forever()

    Thread(target=run_server).start()
