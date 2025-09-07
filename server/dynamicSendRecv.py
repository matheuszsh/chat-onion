import struct

def send_msg(sock, msg: bytes):
    length = len(msg)
    sock.sendall(struct.pack('!I', length))  # envia 4 bytes do tamanho
    sock.sendall(msg)  # envia mensagem

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_msg(sock):
    raw_len = recvall(sock, 4)
    if not raw_len:
        return None
    length = struct.unpack('!I', raw_len)[0]
    return recvall(sock, length)