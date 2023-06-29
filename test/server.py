import socket
import os

HOST = '127.0.0.1'
PORT = 5050
ADDRESS = (HOST, PORT)

def send_file(client_socket, filename):
    file_path = os.path.join('.', filename)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
            client_socket.sendall(data)
        print(f"File '{filename}' sent successfully.")
    else:
        print(f"File '{filename}' does not exist.")

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break

        if command.startswith('download'):
            filename = command.split()[1]
            send_file(client_socket, filename)

    client_socket.close()

if __name__ == '__main__':
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind(ADDRESS)
    Server.listen(5)

    while True:
        client_socket, address = Server.accept()
        print("New client connected: ", address)
        handle_client(client_socket)
