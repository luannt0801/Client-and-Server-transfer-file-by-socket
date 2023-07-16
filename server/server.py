import socket
import os
import time
import ssl
from _thread import *
import threading

from handle_thread import handle_client
from send import send_message

HOST = 'localhost'
PORT = 8000
clients = []

CERTIFICATE_FILE = 'server.crt'
PRIVATE_KEY_FILE = 'server.key'

SERVER_DIRECTORY = 'server'

PID = os.getpid()
print(PID)
# PATH = 'sendFILE/Helloworld.py'

if __name__ == '__main__':

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    # Thực hiện SSL handshake
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTIFICATE_FILE, keyfile=PRIVATE_KEY_FILE)
    secure_socket = context.wrap_socket(server_socket, server_side=True)
    print("Server is ready to listenning . . .")

    while True:
        client_socket, addr = secure_socket.accept()
        clients.append(addr)
        print("Connected:", addr)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
