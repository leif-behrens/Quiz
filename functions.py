import pickle

HEADER = 64
CODING = "utf-8"

def send_msg(_socket, pickle_object):
    """
    :param _socket: socket-Object
    :param pickle_object: Bytes-Object
    :return: None
    """
    _socket.send(str(len(pickle_object)).encode(CODING))
    _socket.send(pickle_object)


def recv_msg(_socket, chunksize=1024):
    """
    :param _socket: socket-Object
    :param chunksize: size of the chunks
    :return: Object (unpickled)
    """
    len_msg = int(_socket.recv(HEADER).decode(CODING))

    msg = b""

    while True:
        if len(msg) == len_msg:
            break

        msg += _socket.recv(chunksize)
    
    return pickle.loads(msg)
