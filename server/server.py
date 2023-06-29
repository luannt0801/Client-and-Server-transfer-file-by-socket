import socket
import os
import time
from _thread import *
import threading

from Func_threading import handle_client
from send import send_message

HOST = 'localhost'
PORT = 8000
clients = []

PID = os.getpid()
print(PID)
# PATH = 'sendFILE/Helloworld.py'

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print("Server đã sẵn sàng lắng nghe...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(addr)
        print("Đã kết nối từ:", addr)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
