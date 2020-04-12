import pickle

HEADER = 20
FORMAT = "utf-8"


def send(_socket, obj):
    msg = pickle.dumps(obj)

    msg_header = bytes(f"{len(msg):<{HEADER}}", FORMAT) + msg
    _socket.send(msg_header)


def recv(_socket, chunksize=32):    
    full_msg = b""
    new_msg = True

    while True:
        msg = _socket.recv(chunksize)

        if new_msg:
            msg_len = int(msg[:HEADER])            
            new_msg = False

        full_msg += msg
        
        if len(full_msg) - HEADER == msg_len:
            return pickle.loads(full_msg[HEADER:])

