import os
import socket
import keyboard

def receive_file(client:socket, file_name):
    download_dir = input("Download to: ")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    else:
        print("Folder already exists!")
    save_path = os.path.join(download_dir, file_name)

    file_length = int(client.recv(1024).decode())
    print(file_length)
    client.send("OK".encode())

    received_bytes = 0

    with open(save_path, 'wb') as file:
        while received_bytes < file_length:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)

def receive_folder(client, folder_name):
    try:
        # os.makedirs(folder_name, exist_ok=True) # create a folder
        download_dir = input("Save as: ")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        else:
            print("Folder already exists!")
        msg = client.recv(1024).decode()
        num_files = int(msg)
        num_files_received = 0
        client.send("OK".encode())
        while num_files_received < num_files:
            # receive name
            name_file_rcv = client.recv(1024).decode()
            # send OK
            client.send("ok".encode())
            # receive size
            file_size = int(client.recv(1024).decode())
            # send OK
            client.send("ok".encode())
            # save
            file_path = os.path.join(download_dir, name_file_rcv)
            with open(file_path, 'wb') as file:
                total_received = 0
                while total_received < file_size:
                    data = client.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    total_received += len(data)
            num_files_received += 1

    except Exception as e:
        print("Error occurred while receiving and writing data:", str(e))

def send_file_list():
    files = os.listdir('.')
    file_list = '     '.join(files)
    return file_list

def menu():
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("+ 1. List files in server directory (ls <folder_name>)          +")
    print("+    ls server : to see all file in server                      +")
    print("+    ls client : to see all file in client                      +")
    print("+    ls <folder_name> : to see all file in folder in server     +")
    print("+ 2. Download file (download <file_name>)                       +")
    print("+ 3. Upload file (upload <file_name>)                           +")
    print("+ 4. Exit (exit server)                                         +")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")