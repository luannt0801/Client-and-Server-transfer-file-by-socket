import socket
import os
import time
from _thread import *
import threading
from message_handle import MessageHandle
import ssl

from send import send_message

HOST = 'localhost'
PORT = 8000
CERTIFICATE_FILE = 'client.crt'

if __name__ == '__main__':
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((HOST, PORT))

    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # context.load_verify_locations(cafile=CERTIFICATE_FILE)
    # secure_socket = context.wrap_socket(Client, server_hostname=HOST)
    # secure_socket.connect((HOST, PORT))
    
    mess0 = Client.recv(1024).decode()
    print(mess0)
    star_msg = "Client say hello"
    Client.send(star_msg.encode())
    data = Client.recv(1024)
    print(data.decode())

    while True:

        # command input
        command = input("Enter command >>")
        if not command:
            break
        else:
            send_message(Client, command.encode())

            # split command
            request, file_name = command.split(" ")   
            print(request + " " + file_name)     

            # list
            if request == 'list':
                print("List file "+ file_name + ":")
                package = Client.recv(1024).decode()
                print(package)

            # download
            if request == 'download':
                package = Client.recv(1024).decode()
                if package == 'OK': # server send "OK" to confirm file exist
                    download_dir = input("Download to: ")

                    if not os.path.exists(download_dir):
                        os.makedirs(download_dir)
                    else:
                        print("Folder already exists!")

                    file_path = os.path.join(download_dir, file_name)
                    with open(file_path, 'wb') as file:
                        while True:
                            data = Client.recv(1024)
                            if not data:
                                break
                            file.write(data)
                            print(f"File '{file_name}' downloaded successfully.")
                    continue
