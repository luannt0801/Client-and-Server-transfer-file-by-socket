import socket
import os
import time
from _thread import *
import threading

from Func_threading import handle_client

HOST = '127.0.0.1'
PORT = 5050
clients = []

PID = os.getpid()
print(PID)
# PATH = 'sendFILE/Helloworld.py'

def start_server():
    host = HOST  # Địa chỉ IP của server
    port = PORT  # Cổng kết nối

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server đã sẵn sàng lắng nghe...")

    while True:
        client_socket, addr = server_socket.accept()
        print(addr)
        clients.append(addr)
        print("Đã kết nối từ:", addr)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    start_server()
