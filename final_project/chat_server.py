import sys
import socket
import select
import json

WORD_LEN_SIZE = 2

def message(data):
    payload = json.dumps(data).encode()
    length = len(payload).to_bytes(WORD_LEN_SIZE, "big")
    return length + payload

def get_packet(buf):
    if len(buf) < WORD_LEN_SIZE:
        return None, buf

    word_len = int.from_bytes(buf[:WORD_LEN_SIZE], "big")
    packet_len = WORD_LEN_SIZE + word_len

    if len(buf) < packet_len:
        return None, buf

    payload = buf[WORD_LEN_SIZE:packet_len]
    remaining = buf[packet_len:]
    
    data = json.loads(payload.decode())
    return data, remaining

def run_server(port):
    read_set = set()
    client_nick = {}
    buffer = {}
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen()
    read_set.add(s)

    while True:
        ready_to_read, _, _ = select.select(read_set, [], [])
        to_remove = []

        for soc in ready_to_read:
            if soc is s:
                conn, addr = s.accept()
                read_set.add(conn)
                buffer[conn] = b""
                client_nick[conn] = None
                print(f"{addr} connected")
                continue

            data = soc.recv(4096)


            if not data:
                nick = client_nick.get(soc)
                addr = soc.getpeername()

                print(f"{addr} ({nick}) disconnected")
                if nick:
                    leave_msg = message({"type": "leave", "nick": nick})
                    for client in read_set:
                        if client not in (s, soc):
                            client.sendall(leave_msg)

                to_remove.append(soc)
                continue

            buffer[soc] += data

            while True:
                pkt, buffer[soc] = get_packet(buffer[soc])
                if pkt is None:
                    break

                pkt_type = pkt.get("type")
                if pkt_type == "hello":
                    nick = pkt.get("nick")
                    client_nick[soc] = nick
                    print(f"{nick}: connected")
                    join_msg = message({"type": "join", "nick": nick})
                    for client in read_set:
                        if client not in (s, soc):
                            client.sendall(join_msg)

                elif pkt_type == "chat":
                    nick = client_nick.get(soc)
                    msg_text = pkt.get("message", "")
                    print(f"{nick}: {msg_text}")
                    chat_msg = message({"type": "chat", "nick": nick, "message": msg_text})
                    for client in read_set:
                        if client not in (s, soc):
                            client.sendall(chat_msg)


                elif pkt_type == "leave":
                    nick = client_nick.get(soc)
                    print(f"{nick}: left")
                    leave_msg = message({"type": "leave", "nick": nick})
                    for client in read_set:
                        if client not in (s, soc):
                            client.sendall(leave_msg)

                    to_remove.append(soc)
                    break 


        for soc in to_remove:
            read_set.discard(soc)
            buffer.pop(soc, None)
            client_nick.pop(soc, None)

            soc.close()



def main(argv):
    port = int(argv[1])
    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
