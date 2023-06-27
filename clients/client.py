import socket
import os
import time
from _thread import *
import threading
from message_handle import MessageHandle

HOST = '127.0.0.1'
PORT = 5050
if __name__ == '__main__':
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((HOST, PORT))
    data = Client.recv(1024).decode()
    print(data)
    while True:
        data = Client.recv(1024)
        print(data)
        MessageHandle(data)