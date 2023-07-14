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
    # # Gửi tên thư mục đến máy chủ
    # folder_name = os.path.basename(folder_path)
    # sock.send(folder_name.encode())

    # Lặp qua tất cả các tệp trong thư mục và gửi chúng tới máy chủ
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            send_file(sock, file_path)

# Hàm gửi tệp từ máy khách tới máy chủ
def send_file(sock, file_path):
    # # Gửi tên tệp đến máy chủ
    # file_name = os.path.basename(file_path)
    # sock.send(file_name.encode())

    # Gửi nội dung tệp tới máy chủ
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(1024), b''):
            sock.send(chunk)

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


