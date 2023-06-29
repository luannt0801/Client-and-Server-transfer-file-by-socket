import socket

def send_message(client: socket.socket,
                #  content_type: bytes,
                #  ID: bytes,
                #  check: bytes,
                 command):
    client.send(
        # content_type +
                # ID +
                # check +
                command)