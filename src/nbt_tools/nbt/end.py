

def byte_length() -> int:
    return 1


def read(buf):
    return 'end'


def write(data):
    return int(0).to_bytes(byte_length(), byteorder='big')
