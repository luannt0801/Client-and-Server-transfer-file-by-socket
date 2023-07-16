import socket
import os
import time
import ssl
from send import send_message

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