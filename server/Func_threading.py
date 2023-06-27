import socket
import os
import time

def handle_client(server: socket.socket,):
    msg = "Day la tin nhan tu server"
    server.send(msg.encode())

    time.sleep(5)

    msg = "Day la tin nhan thu 2 tu server"
    server.send(msg.encode())

    # data = server.recv(1024).decode()
    # print(data)
