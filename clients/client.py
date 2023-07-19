import socket
from _thread import *
import threading
import ssl

from func_handle_data import *

from send import send_message

HOST = 'localhost'
PORT = 8000
CERTIFICATE_FILE = 'client.crt'
socket_lock = threading.Lock()


if __name__ == '__main__':
    nonsercue_Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=CERTIFICATE_FILE)
    Client = context.wrap_socket(nonsercue_Client, server_hostname=HOST)
    Client.connect((HOST, PORT))
    
    mess0 = Client.recv(1024).decode()
    print(mess0)
    star_msg = "Client say hello"
    Client.send(star_msg.encode())
    data = Client.recv(1024)
    print(data.decode())
    menu()

    while True:

        # command input
        command = input("Enter command >>")
        if not command:
            break
        else:
            send_message(Client, command.encode())

            # split command
            if len(command.split(" ")) == 2:
                request, file_name = command.split(" ")   
            else:
                request =""
                file_name =""

            # list
            if request == "ls":
                if file_name == "client":
                    Client.recv(1024).decode()
                    print(send_file_list())
                    continue
                elif file_name == "server":
                    package = Client.recv(1024).decode()
                    print(package)
                    continue
                elif file_name != "client" or file_name != "server":
                    package = Client.recv(1024).decode()
                    print(package)
                    continue

            # download  
            if request == "download":
                check_file = Client.recv(1024).decode()
                check_done = "OK"
                send_message(Client, check_done.encode())
                # save file
                if check_file == 'file':
                    receive_file(Client, file_name)
                if check_file == 'folder':
                    receive_folder(Client, file_name)
                # if check_file == 'not found'

            # upload
            if request == "upload":
                file_check = check_file_type(file_name)
                Client.send(file_check.encode())
                # OK
                Client.recv(1024)
                if file_check == "file":
                    send_file(Client, file_name)
                if file_check == "folder":
                    send_folder(Client, file_name)

            # exit
            if request == "exit":
                if file_name == "server":
                    break
                else:
                    print("ERROR COMMAND")
            
            if request not in ["ls", "download", "upload", "exit"]:
                print("ERROR COMMAND!!")
                continue