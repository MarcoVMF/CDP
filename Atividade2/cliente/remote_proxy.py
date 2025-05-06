import requests
import json
from base64 import b64encode

class RemoteFileProxy:
    def __init__(self, url, username, password):
        userpass = f"{username}:{password}"
        self.auth_header = "Basic " + b64encode(userpass.encode()).decode()
        self.url = url

    def call(self, method, *args):
        payload = json.dumps({"method": method, "args": args})
        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json"
        }
        response = requests.post(self.url, data=payload, headers=headers)
        return response.json()