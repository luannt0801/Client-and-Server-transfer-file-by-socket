import socket

HOST = '127.0.0.1'
PORT = 5050
ADDRESS = (HOST, PORT)

def receive_file(server_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"File '{filename}' received successfully.")

if __name__ == '__main__':
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect(ADDRESS)

    while True:
        command = input("Enter command (download <filename>): ")
        if command == 'exit':
            break

        Client.sendall(command.encode())

        if command.startswith('download'):
            filename = command.split()[1]
            receive_file(Client, filename)

    Client.close()
