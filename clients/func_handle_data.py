import os
import socket
import keyboard
from send import *

def check_file_type(file_path):
    if os.path.isfile(file_path):
        return "file"
    elif os.path.isdir(file_path):
        return "folder"
    else:
        return "not_found"

def send_folder(sock, folder_path):
    try:
        # send dir
        download_dir = input("save as: ")
        sock.send(download_dir.encode())
        # OK
        sock.recv(1024)
        # send len file
        files_in_folder = os.listdir(folder_path)
        num_files = len(files_in_folder)
        sock.send(str(num_files).encode())
        # OK
        sock.recv(1024)
        # start send
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
                    bytes = 0
                    while bytes < len_file:
                        sock.send(data)
                        data = file.read(1024)
                        bytes +=1
    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def send_file(sock, file_path):
    try:
        download_dir = input("Upload to: ")
        sock.send(download_dir.encode())
        sock.recv(1024)
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            len_file = len(data) # send lenght of file
            send_message(sock, (str(len_file)).encode())
            sock.recv(1024)
            bytes = 0
            while bytes < len_file:
                sock.send(data)
                data = file.read(1024)
                bytes +=1
    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def receive_file(client:socket, file_name):
    download_dir = input("Download to: ")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    else:
        print("Folder already exists!")
    save_path = os.path.join(download_dir, file_name)

    file_length = int(client.recv(1024).decode())
    print(file_length)
    client.send("OK".encode())

    received_bytes = 0

    with open(save_path, 'wb') as file:
        while received_bytes < file_length:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)

def receive_folder(client, folder_name):
    try:
        # os.makedirs(folder_name, exist_ok=True) # create a folder
        download_dir = input("Save as: ")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        else:
            print("Folder already exists!")
        msg = client.recv(1024).decode()
        num_files = int(msg)
        num_files_received = 0
        client.send("OK".encode())
        while num_files_received < num_files:
            # receive name
            name_file_rcv = client.recv(1024).decode()
            # send OK
            client.send("ok".encode())
            # receive size
            file_size = int(client.recv(1024).decode())
            # send OK
            client.send("ok".encode())
            # save
            file_path = os.path.join(download_dir, name_file_rcv)
            with open(file_path, 'wb') as file:
                total_received = 0
                while total_received < file_size:
                    data = client.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    total_received += len(data)
            num_files_received += 1

    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def send_file_list():
    files = os.listdir('.')
    file_list = '     '.join(files)
    return file_list

def menu():
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("+ 1. List files in server directory (ls <folder_name>)          +")
    print("+    ls server : to see all file in server                      +")
    print("+    ls client : to see all file in client                      +")
    print("+    ls <folder_name> : to see all file in folder in server     +")
    print("+ 2. Download file (download <file_name>)                       +")
    print("+ 3. Upload file (upload <file_name>)                           +")
    print("+ 4. Exit (exit server)                                         +")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")