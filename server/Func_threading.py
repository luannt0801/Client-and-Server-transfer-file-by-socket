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

def send_folder(sock, folder_path):
    try:
        files_in_folder = os.listdir(folder_path)
        num_files = len(files_in_folder)
        print(num_files)
        sock.send(str(num_files).encode())
        test = sock.recv(1024)
        print(test.decode())
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                print(file_path)
                sock.send(file_name.encode())
                sock.recv(1024)
                with open(file_path, 'rb') as file:
                    data = file.read(1024)
                    len_file = len(data) # send lenght of file
                    send_message(sock, (str(len_file)).encode())
                    sock.recv(1024)
                    while data:
                        sock.send(data)
                        data = file.read(1024)
    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def send_file(sock, file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            len_file = len(data) # send lenght of file
            send_message(sock, (str(len_file)).encode())
            sock.recv(1024)
            while data:
                sock.send(data)
                data = file.read(1024)
    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def check_file_type(file_path):
    if os.path.isfile(file_path):
        return "file"
    elif os.path.isdir(file_path):
        return "folder"
    else:
        return "not_found"

def handle_client(server: socket.socket,):
    # # Thực hiện SSL handshake
    # context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # context.load_cert_chain(certfile=CERTIFICATE_FILE, keyfile=PRIVATE_KEY_FILE)
    # secure_socket = context.wrap_socket(server, server_side=True)

    # welcome
    msg0 = "--- Welcome to server ---\nDownload/Upload + file name | ls\nserver:"
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

        # list
        if request.startswith("ls"):
            folder_path = request.split("ls")[1].strip()
            print(folder_path)
            files = os.listdir(folder_path)
            file_list = ' '.join(files)
            print(file_list)
            send_message(server, file_list.encode())

        # down load
        if command == "download":
            file_check = check_file_type(filename)
            send_message(server, file_check.encode())
            ack_msg = server.recv(1024).decode()
            if ack_msg == "OK":
                if file_check == "file":
                    send_file(server, filename)
                if file_check == "folder":
                    send_folder(server, filename)            


