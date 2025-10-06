import socket

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = ('', 28333)
s.bind(port)

s.listen()

res = "HTTP/1.1 200 OK\r\n\
Content-Type: text/plain \r\n\
Content-Length: 6 \r\n\
Connection: close\r\n\r\nHello!"



while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    d = new_socket.recv(1000).decode()

    print(new_conn[1]) #see if client was conencting properly
    new_socket.sendall(res.encode())
    if d == "\r\n\r\n":
        break
  
    new_socket.close()
