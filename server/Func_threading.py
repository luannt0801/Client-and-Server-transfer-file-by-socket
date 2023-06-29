import socket
import os
import time
import ssl
from send import send_message

CERTIFICATE_FILE = 'server.crt'
PRIVATE_KEY_FILE = 'server.key'

SERVER_DIRECTORY = 'server'

def send_file_list():
    files = os.listdir('.')
    file_list = '     '.join(files)
    return file_list


def handle_client(server: socket.socket,):
    # # Thực hiện SSL handshake
    # context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # context.load_cert_chain(certfile=CERTIFICATE_FILE, keyfile=PRIVATE_KEY_FILE)
    # secure_socket = context.wrap_socket(server, server_side=True)

    # welcome
    msg0 = "--- Welcome to server ---\nDownload/Upload + file name | cd & cd .. to move"
    server.send(msg0.encode())
    start_msg = server.recv(1024)
    # time.sleep(5)
    print(start_msg.decode())
    file_list = send_file_list()
    server.send(file_list.encode())

    # start
    while True:
        #list file
        package = server.recv(1024).decode()
        print(package)
        command, filename = package.split()
        # list
        if package.startswith("list"):
            folder_path = package.split("list")[1].strip()
            print(folder_path)
            files = os.listdir(folder_path)
            file_list = ' '.join(files)
            print(file_list)
            send_message(server, file_list.encode())

        # #download
        # elif command == "download":
        #     file_name = filename
        #     if os.path.isfile(file_name):
        #         server.send('OK'.encode())
        #         with open(file_name, 'rb') as file:
        #             data = file.read(1024)
        #             while data:
        #                 server.send(data)
        #                 data = file.read(1024)
        #     else:
        #         server.send('File not found'.encode())
