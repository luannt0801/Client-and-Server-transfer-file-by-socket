import socket
import os
import time
from _thread import *

HOST = '127.0.0.1'
PORT = 5050
ADDR =(HOST, PORT)

class Client:
    def __init__(self):
        self.server_address = None
    
    def connect(self):
        self.server_address = ADDRESS
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_address)

        print("Connected to server.")

        while True:
            command = input("Enter command: ")
            client_socket.send(command.encode())

            if command == 'download':
                file_list = client_socket.recv(1024).decode()
                print("Available files:")
                print(file_list)

                filename = input("Enter filename to download: ")
                client_socket.send(filename.encode())

                response = client_socket.recv(65535).decode()
                if response == 'OK':
                    file_path = './downloads/' + filename
                    with open(file_path, 'wb') as file:
                        while True:
                            data = client_socket.recv(65535)
                            if not data:
                                break
                            file.write(data)
                    print("Download complete.")
                else:
                    print("File not found.")

            elif command == 'upload':
                file_list = client_socket.recv(1024).decode()
                print("Available files:")
                print(file_list)

                filename = input("Enter filename to upload: ")
                client_socket.send(filename.encode())

                response = client_socket.recv(1024).decode()
                if response == 'OK':
                    file_path = './uploads/' + filename
                    with open(file_path, 'rb') as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            client_socket.send(data.decode())
                    print("Upload complete.")
                else:
                    print("Server rejected the upload.")

        client_socket.close()

if __name__ == '__main__':
    client = Client()
    client.connect()