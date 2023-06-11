import socket
import os
import time
from _thread import *
import threading

HOST = '127.0.0.1'
PORT = 5050
ADDR =(HOST, PORT)
num_clients = 5
clients = []

#PID
PID = os.getpid()
print(PID)
# PATH = 'sendFILE/Helloworld.py'

HOST = '127.0.0.1'
PORT = 5050
ADDRESS = (HOST, PORT)


class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

    # start connect

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server is listening . . .")

        while True:
            client_socket, address = self.sock.accept()
            print("New client connected: ", address)
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    
    # send file

    def send_file(self, client_socket, file_path):
        print('File is sending to client')
        with open(file_path, 'rb') as file:
            data = file.read(65535)
            while data:
                client_socket.send(data)
                data = file.read(1024)

    # check command from client and enforcement

    def handle_client(self, client_socket, address):
        files = os.listdir('.')
        file_list = '\n'.join(files)
        client_socket.send(file_list.encode())
        try:
            request = client_socket.recv(1024).decode()
            print('Client' + str(address)+ 'send: ' + str(request))

            # Xử lý yêu cầu từ client

            if request == 'download':
                filename = client_socket.recv(1024).decode()
                if filename in files:
                    client_socket.send('OK'.encode())
                    self.send_file(client_socket, filename)
                else:
                    client_socket.send('File not found'.encode())
            elif request == 'upload':
                filename = client_socket.recv(1024).decode()
                client_socket.send('OK'.encode())
                with open(filename, 'wb') as file:
                    data = client_socket.recv(1024)
                    while data:
                        file.write(data)
                        data = client_socket.recv(1024)            
        except ConnectionResetError:
            print(f"Connection reset by peer: {address}")

        #     # Xử lý lỗi kết nối bị đóng

            
        # except KeyboardInterrupt:
        #     print("Server stopped by user.")
            
        #     # Thực hiện các tác vụ dừng server một cách an toàn (đóng socket, lưu dữ liệu, v.v.)

        # finally:
        #     client_socket.close()

        # if request == 'download':
        #     filename = client_socket.recv(1024).decode('utf-8')
        #     if filename in files:
        #         client_socket.send('OK'.encode('utf-8'))
        #         self.send_file(client_socket, filename)
        #     else:
        #         client_socket.send('File not found'.encode('utf-8'))
        # elif request == 'upload':
        #     filename = client_socket.recv(1024).decode('utf-8')
        #     client_socket.send('OK'.encode('utf-8'))
        #     with open(filename, 'wb') as file:
        #         data = client_socket.recv(1024)
        #         while data:
        #             file.write(data)
        #             data = client_socket.recv(1024)

        # print(f"Disconnected from client: {address}")

if __name__ == '__main__':
    server = Server(HOST, PORT)
    server.start_server()