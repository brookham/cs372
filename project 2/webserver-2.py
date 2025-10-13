import socket
import os
import mimetypes

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = ('', 28333)
s.bind(port)

s.listen()

# res = "HTTP/1.1 200 OK\r\n\
# Content-Type: text/plain \r\n\
# Content-Length: 6 \r\n\
# Connection: close\r\n\r\nHello!"

def parse(req):
    end = req.find("\r\n\r\n")
    line = req.split("\r\n")
    # if end not in line:
    #     print(line)
    full_path = (line[0].split(" "))[-2]

    file_name = os.path.split(full_path)[-1]

    # name, type = os.path.splitext(file_name)
    mime_type, encode = mimetypes.guess_type(file_name)

    try:
        with open(req, "rb") as fp:
            data = fp.read()
            length = len(data)    
            res = f"HTTP/1.1 200 OK\r\n\
Content-Type: {mime_type} \r\n\
Content-Length: {length} \r\n\
Connection: close\r\n\r\nHello!"
            return res

    except:
        return "HTTP/1.1 404 Not Found\r\n\
Content-Type: text/plain\r\n\
Content-Length: 13\r\n\
Connection: close\r\n\r\n404 not found"




while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    d = new_socket.recv(1000).decode("ISO-8859-1")
    print(parse(d))


    new_socket.sendall(parse(d).encode("ISO-8859-1"))

    if d == "\r\n\r\n":
        new_socket.close()
    

    
