from chatuicurses import init_windows, read_command, print_message, end_windows

import socket
import threading
import sys
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


def main(argv):
    try: 
        name = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        print("usage: chat_client.py name host port", file=sys.stderr)
        return 1

    sock = socket.socket()
    
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")

    
    init_windows()
    
    hello_msg = message({"type": "hello", "nick": name})
    sock.sendall(hello_msg)
    
    recv_buffer = b''

    def send():
        while True:
          msg = read_command(f"{name}> ")

          if msg:
              
            if "/q" in msg:
              leave_msg = message({"type": "leave", "nick": name})
              sock.sendall(leave_msg)
              sock.close()
              break
            else:
                chat_msg = message({"type": "chat", "message": msg})
                sock.sendall(chat_msg)

    def receive():
        nonlocal recv_buffer
        while True:
                data = sock.recv(4096)
                
                recv_buffer += data
                
                while True:
                    pkt, recv_buffer = get_packet(recv_buffer)
                    if pkt is None:
                        break
                    
                    pkt_type = pkt.get("type")
                    
                    if pkt_type == "chat":
                        nick = pkt.get("nick", "unknown")
                        msg_text = pkt.get("message", "")
                        print_message(f"{nick}: {msg_text}")
                    
                    elif pkt_type == "join":
                        nick = pkt.get("nick", "unknown")
                        print_message(f">>> {nick} connected")
                    
                    elif pkt_type == "leave":
                        nick = pkt.get("nick", "unknown")
                        print_message(f"<<< {nick} left")

    t1 = threading.Thread(target=send, daemon=True)
    t2 = threading.Thread(target=receive, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    end_windows()
    sock.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))