# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select



def run_server(port):
    read_set = set()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", port))
    s.listen()

    read_set.add(s)


    while True:
        ready_to_read, _, _, = select.select(read_set, [], [])

        for soc in ready_to_read:
            if soc == s:
                listen_socket = soc.accept()
                new_sock = listen_socket[0]
                read_set.add(new_sock)
                s_host, s_port = new_sock.getpeername()
                print(f"{s_host}, {s_port}: connected")
            else:
                data = soc.recv(1000)
                print(f"({s_host}, {s_port}) {len(data)}: {data}")

                if len(data) == 0:
                    read_set.remove(soc)
                    print(f"{s_host}, {s_port}: disconnected")
            
        

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
