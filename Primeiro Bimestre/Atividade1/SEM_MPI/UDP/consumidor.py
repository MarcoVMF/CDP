import socket
import struct
import base64
import xml.etree.ElementTree as ET

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
            print("Recebido [serializado base64]:")
        elif data.startswith(b'XML:'):
            xml_bytes = data[4:]
            print("Recebido [xml string]:")
        else:
            print("Formato desconhecido")
            continue

        try:
            root = ET.fromstring(xml_bytes)
            for elem in root:
                tag = elem.tag.split('}')[-1]
                print(f"{tag} => {elem.text}")
        except ET.ParseError as e:
            print("Erro ao fazer parse do XML:", e)

        print("-" * 30)


if __name__ == "__main__":
    main()