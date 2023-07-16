# SERVER TO CLIENT

## Chạy chương trình

Server:
```
cd server/
sudo python3 server.py
```

Các Clients:
```
cd clients/
sudo python3 client.py
```

## Communication between client and server

![alt](pic/client-server-1.png)

## Flow data

![alt](pic/dataflow.png)

**SERVER**
1. Connect to client by socket (socket, threading) + SSL
2. As soon as a thread connects, the server will call the **handle_client function** to execute
3. Check **request** from client and execute
   **request** = "download"
   **request** = "upload"

**CLIENTS**
1. Connect to server
2. Send command
3. Receive data and save