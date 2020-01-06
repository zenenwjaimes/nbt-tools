

def byte_length() -> int:
    return 2


def read(buf):
    data = buf.read(byte_length())
    length = (data[0] << 8) | data[1]
    string = buf.read(length).decode("utf-8")

    return string
