import socket
import os
import time
from _thread import *

HOST = '127.0.0.1'
PORT = 5050
ADDR =(HOST, PORT)
num_clients = 5
clients = []

#PID
PID = os.getpid()
print(PID)
# PATH = 'sendFILE/Helloworld.py'

def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(f"{threadName}: {time.ctime(time.time())}")

def send_file(conn, file_path):
    # file_path = PATH
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            conn.send(data)
            data = file.read(1024)

def handle_client(conn, addr):
    print(f"Connected to client: {addr}")
    files = os.listdir('.')
    file_list = '\n'.join(files)
    conn.send(file_list.encode())

    request = conn.recv(1024).decode()
    if request == 'download':
        filename = conn.recv(1024).decode()
        if filename in files:
            conn.send('OK'.encode())
            send_file(conn, filename)
        else:
            conn.send('File not found'.encode())
    elif request == 'upload':
        filename = conn.recv(1024).decode()
        conn.send('OK'.encode())
        with open(filename, 'wb') as file:
            data = conn.recv(1024)
            while data:
                file.write(data)
                data = conn.recv(1024)

    print(f"Disconnected from client: {addr}")
    conn.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    start_server(HOST, PORT)

