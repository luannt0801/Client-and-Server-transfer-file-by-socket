import socket
import os
import time
import ssl
from send import send_message
from func_send import *

def handle_client(server: socket.socket,):
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


