with open('tcp_addrs_0.txt', 'r') as file:
    ip = file.read()

with open('tcp_data_0.dat', 'rb') as file:
    tcp_data = file.read()
    tcp_length = len(tcp_data)


split_file = ip.split(" ")
source = split_file[0]
dest = split_file[1]

tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]


def bytestring(file):
    file = file.split(".")

    for byte in range(len(file)):
        file[byte] = int(file[byte])

    file = bytes(file)


    return file


def pseudo_header():
    header = b''
    header += bytestring(source)
    header += bytestring(dest)
    header += b'\x00'
    header += b'\x06'
    header += tcp_length.to_bytes(2, "big")

    return header

def checksum():

    og_checksum = int.from_bytes(tcp_data[16:18], "big")

    pseudo_and_tcp = pseudo_header() + tcp_zero_cksum

    print(og_checksum)
    print(pseudo_and_tcp)


checksum()
