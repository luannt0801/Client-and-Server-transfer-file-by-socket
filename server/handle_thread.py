import socket
import os
import time
import ssl
from send import send_message
from func_send import *

def handle_client(server: socket.socket,):
    # welcome
    msg0 = "--- Welcome to SSL server ---\nserver:"
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
        if len(request.split(" ")) == 2:
                command, filename = request.split(" ")   
        else:
            command =""
            filename =""

        # list
        if request.startswith("ls"):
            folder_path = request.split("ls")[1].strip()
            print(folder_path)
            if not folder_path:
                msg = "Invalid folder path."
                print(msg)
                send_message(server, str(msg).encode())
            else:
                if folder_path == "server":
                    server_list = send_file_list()
                    server.send(server_list.encode())
                elif folder_path == "client":
                    server.send("OK".encode())
                elif folder_path != "client" or folder_path != "server":
                    error = "File/Folder is not exist!!"
                    send_message(server, error.encode())

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

        # upload
        if command == "upload":
            file_check = server.recv(1024).decode()
            print(file_check)
            server.send("OK".encode())
            if file_check == "file":
                receive_file(server, filename)
            if file_check == "folder":
                receive_folder(server, filename)