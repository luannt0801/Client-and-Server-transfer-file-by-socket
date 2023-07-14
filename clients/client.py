import socket
import os
import time
from _thread import *
import threading
from message_handle import MessageHandle
import ssl

from send import send_message

HOST = 'localhost'
PORT = 8000
CERTIFICATE_FILE = 'client.crt'

def receive_file(sock, file_name, save_dir):
    # file_received = sock.recv(65536).decode()  # Nhận tên file từ client
    # print(file_received)
    # save_path = os.path.join(save_dir, file_received)
    save_path = os.path.join(save_dir, file_name)
    with open(save_path, 'wb') as file:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            file.write(data)

def receive_folder(sock, folder_name, save_dir):
    # folder_info = sock.recv(1024).decode()  # Nhận thông tin thư mục từ client
    # print(folder_info)
    # folder_name = folder_info.split()[1]
    # folder_path = os.path.join(save_dir, folder_name)
    # os.makedirs(folder_path, exist_ok=True)
    folder_path = os.path.join(save_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    # Nhận tất cả các file trong thư mục từ client
    while True:
        receive_file(sock,folder_name ,folder_path)
        # Kiểm tra xem còn file nữa không
        data = sock.recv(1024)
        if not data:
            break

if __name__ == '__main__':
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((HOST, PORT))

    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # context.load_verify_locations(cafile=CERTIFICATE_FILE)
    # secure_socket = context.wrap_socket(Client, server_hostname=HOST)
    # secure_socket.connect((HOST, PORT))
    
    mess0 = Client.recv(1024).decode()
    print(mess0)
    star_msg = "Client say hello"
    Client.send(star_msg.encode())
    data = Client.recv(1024)
    print(data.decode())

    while True:

        # command input
        command = input("Enter command >>")
        if not command:
            break
        else:
            send_message(Client, command.encode())

            # split command
            request, file_name = command.split(" ")   
            print(request + " " + file_name)     

            # list
            if request == "ls":
                print("List file "+ file_name + ":")
                package = Client.recv(1024).decode()
                print(package)
                
            if request == "download":
                check_file = Client.recv(1024).decode()
                print(check_file) # test
                check_done = "OK"
                send_message(Client, check_done.encode())
                # create folder save
                download_dir = input("Download to: ")
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                else:
                    print("Folder already exists!")
                # save file
                if check_file == 'file':
                    receive_file(Client, file_name, download_dir)
                if check_file == 'folder':
                    receive_folder(Client, file_name, download_dir)
                # if check_file == 'not found'

