import socket
import struct
import base64
import xml.etree.ElementTree as ET

# AF_INET -> IPV4
# SOCK_DGRAM -> UDP/IP
# SOL_SOCKET -> Explicita a configuração a nível de socket
# SO_REUSEADDR -> Permite reutilizar o endereço (mesmo que ela já esteja ou futuramente vá ser usada)
# inet_aton -> Conversão para formato binário
# INADDR_ANY -> Usa qualquer interface local disponível
# IPPROTO_IP -> Explicita a configuração a nível de ip
# IP_ADD_MEMBERSHIP -> Adiciona esse ip a um grupo multicast 



MULTICAST_IP = '224.0.0.1'
PORT = 5007

NAMESPACES = {
    'pessoas': 'http://example.com/pessoas',
    'pers': 'http://example.com/pers'
}

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('', PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(1024)

        if data.startswith(b'B64:'):
            xml_bytes = base64.b64decode(data[4:])
            print("Recebido [serializado base64]:", flush=True)
        elif data.startswith(b'XML:'):
            xml_bytes = data[4:]
            print("Recebido [xml string]:", flush=True)
        else:
            print("Formato desconhecido", flush=True)
            continue

        try:
            root = ET.fromstring(xml_bytes)
            for elem in root:
                tag = elem.tag.split('}')[-1]
                print(f"{tag} => {elem.text}", flush=True)
        except ET.ParseError as e:
            print("Erro ao fazer parse do XML:", e, flush=True)

        print("-" * 30, flush=True)


if __name__ == "__main__":
    main()
