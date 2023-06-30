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
    msg0 = "--- Welcome to server ---\nDownload/Upload + file name | cd & cd .. to move\nserver:"
    server.send(msg0.encode())
    start_msg = server.recv(1024)
    # time.sleep(5)
    print(start_msg.decode())
    file_list = send_file_list()
    server.send(file_list.encode())

    # start
    while True:
        request = server.recv(1024).decode()
        print(request)
        command, filename = request.split()
        print(command)
        print("\n")
        print(filename)

        # list
        if request.startswith("list"):
            folder_path = request.split("list")[1].strip()
            print(folder_path)
            # check folder exists
            if not os.path.exists(folder_path):
                error_message = f"Folder '{folder_path}' does not exist."
                send_message(server, error_message.encode())
            else:
                files = os.listdir(folder_path)
                file_list = '   '.join(files)
                print(file_list)
                send_message(server, file_list.encode())

        if command == 'download':
            if os.path.isfile(filename):
                send_message(server, 'OK'.encode())
                with open(filename, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        server.send(data)
                        data = file.read(1024)
                print(f"File '{filename}' sent successfully.")
            else:
                send_message(server, 'File not found'.encode())
                print("File not found on the server.")


