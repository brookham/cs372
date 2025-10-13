import socket

import mimetypes

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = ('', 28333)
s.bind(port)

s.listen()


def parse(req):
    full_path = req.split("HTTP")[0].split("GET")[1]

    file_name = full_path.split("/")[-1].strip()

    mime_type, encode = mimetypes.guess_type(file_name)

    try:
        with open(file_name, "rb") as fp:
            data = fp.read().decode("ISO-8859-1")
            length = len(data)  

            res = f"HTTP/1.1 200 OK\r\n\
Content-Type: {mime_type} \r\n\
Content-Length: {length} \r\n\
Connection: close\r\n\r\n{data}!"
            return res

    except:
        res = "HTTP/1.1 404 Not Found\r\n\
Content-Type: text/plain\r\n\
Content-Length: 13\r\n\
Connection: close\r\n\r\n404 not found"
        return res




while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    d = new_socket.recv(1000).decode("ISO-8859-1")
    print(parse(d))


    new_socket.sendall(parse(d).encode("ISO-8859-1"))
    new_socket.close()

    # if "" in d:
    #     break

    

    
