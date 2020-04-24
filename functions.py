import pickle
import os
import csv

HEADER = 20
FORMAT = "utf-8"


def send(_socket, obj):
    msg = pickle.dumps(obj)

    msg_header = bytes(f"{len(msg):<{HEADER}}", FORMAT) + msg
    _socket.send(msg_header)


def recv(_socket, chunksize=512):
    full_msg = b""
    new_msg = True

    while True:
        msg = _socket.recv(chunksize)

        if not msg:
            return msg
        
        if new_msg:
            msg_len = int(msg[:HEADER])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADER == msg_len:
            return pickle.loads(full_msg[HEADER:])


def csv_import(_path, _delimiter):
    if os.path.isfile(_path):
        try:
            with open(_path) as f:
                reader = csv.reader(f, delimiter=_delimiter)
                data = [d for d in reader]

                return data

        except:
            return None
    
    else:
        return None
