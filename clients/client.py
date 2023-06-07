import socket
import os
import time
from _thread import *

HOST = '127.0.0.1'
PORT = 5050
ADDR =(HOST, PORT)

def receive_file(conn, filename):
    with open(filename, 'wb') as file:
        data = conn.recv(1024)
        while data:
            file.write(data)
            data = conn.recv(1024)

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server: {host}:{port}")

    file_list = client_socket.recv(1024).decode()
    print(f"Available files and directories:\n{file_list}")

    request = input("Enter 'download' to download a file, 'upload' to upload a file, or 'exit' to quit: ")
    client_socket.send(request.encode())

    if request == 'download':
        filename = input("Enter the filename to download: ")
        client_socket.send(filename.encode())
        response = client_socket.recv(1024).decode()
        if response == 'OK':
            receive_file(client_socket, filename)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print("File not found on the server.")
    elif request == 'upload':
        filename = input("Enter the filename to upload: ")
        client_socket.send(filename.encode())
        response = client_socket.recv(1024).decode()
        if response == 'OK':
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
            print(f"File '{filename}' uploaded successfully.")
        else:
            print("Error in uploading the file.")

    client_socket.close()

if __name__ == "__main__":
    start_client(HOST, PORT)