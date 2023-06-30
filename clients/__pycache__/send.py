import socket

def send_message(server: socket.socket,
                #  content_type: bytes,
                #  ID: bytes,
                #  check: bytes,
                 payload):
    server.send(
        # content_type +
        # ID +
        # check +
        payload)