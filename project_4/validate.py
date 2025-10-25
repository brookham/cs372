
i = 0
while i <= 9:
    with open(f"tcp_addrs_{i}.txt", 'r') as file:
        ip = file.read()

    with open(f"tcp_data_{i}.dat", 'rb') as file:
        tcp_data = file.read()
        tcp_length = len(tcp_data)

    split_file = ip.split(" ")
    source = split_file[0]
    dest = split_file[1]

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
        tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
        og_cksum = int.from_bytes(tcp_data[16:18], "big")

        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'

        pseudo_and_tcp = pseudo_header() + tcp_zero_cksum
        offset = 0
        total = 0

        while offset < len(pseudo_and_tcp):
            word = int.from_bytes(pseudo_and_tcp[offset:offset + 2], "big")
            total += word
            total = (total & 0xffff) + (total >> 16)
            offset += 2

        return ((~total) & 0xffff), og_cksum


    def checker():
        calculated, og = checksum()

        if calculated == og:
            print("PASS")
        else:
            print("FAIL")
    
   

    checker()
    i += 1
