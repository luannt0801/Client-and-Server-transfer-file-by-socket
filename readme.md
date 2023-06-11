# SERVER TO CLIENT

## Chạy chương trình

Server:
```
cd server/
python3 server.py
```

Các Clients:
```
cd client/
python3 Client.py
```

## Communication between client and server
![alt](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.javatpoint.com%2Fsocket-programming&psig=AOvVaw3qlTE8e5ztuXHX9fT8qEjl&ust=1686582110867000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCKjc7o6-u_8CFQAAAAAdAAAAABAE)


**SERVER**
1. Connect to client by socket (socket, threading)
2. As soon as a thread connects, the server will call the **handle_client function** to execute
3. Check **request** from client and execute
   **request** = "download"
   **request** = "upload"

**CLIENTS**
1. Connect to server
2. Send command
3. Receive data and save - not done

####***Note**
Các việc cần làm:
+ Thêm các lệnh để tìm file:
    Command 'cd' để mở một thư mục
    Lệnh 'rm' để xoá file trên server
    ...
+ Mã hoá cho từng kết nối giữa Client và Server
    Sử dụng OPEN VPN hoặc OPEN SSL/TLS