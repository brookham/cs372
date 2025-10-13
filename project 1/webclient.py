import socket

s = socket.socket()

server = "localhost", 28333
s.connect(server)

req = "GET / HTTP/1.1\r\n\
Host: localhost\r\n\
Connection: close\r\n\r\n"

s.sendall(req.encode())

while True:
    d = s.recv(4090)
    print(d.decode())
    if len(d) == 0:
        s.close()