import socket
import xml.etree.ElementTree as ET
import base64
import time

MULTICAST_IP = '224.0.0.1'
PORT = 5007

NAMESPACES = {
    'pessoas': 'http://example.com/pessoas',
    'pers': 'http://example.com/pers'
}

def criar_xml():
    ET.register_namespace('pessoas', NAMESPACES['pessoas'])
    ET.register_namespace('pers', NAMESPACES['pers'])

    pessoa = ET.Element('pessoa', {'pessoas:id': '123456789'})
    nome = ET.SubElement(pessoa, '{http://example.com/pessoas}nome')
    nome.text = 'Smith'
    place = ET.SubElement(pessoa, '{http://example.com/pers}place')
    place.text = 'Londres'
    ano = ET.SubElement(pessoa, '{http://example.com/pers}ano')
    ano.text = '1984'
    return pessoa

def enviar_base64_xml(sock):
    pessoa = criar_xml()
    xml_str = ET.tostring(pessoa)
    encoded = base64.b64encode(xml_str)
    
    mensagem = b'B64:' + encoded
    sock.sendto(mensagem, (MULTICAST_IP, PORT))

def enviar_xml_string(sock):
    pessoa = criar_xml()
    xml_str = ET.tostring(pessoa)
    mensagem = b'XML:' + xml_str
    sock.sendto(mensagem, (MULTICAST_IP, PORT))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    while True:
        print("Enviando XML serializado...")
        enviar_base64_xml(sock)
        time.sleep(2)

        print("Enviando XML como string...")
        enviar_xml_string(sock)
        time.sleep(2)

if __name__ == "__main__":
    main()