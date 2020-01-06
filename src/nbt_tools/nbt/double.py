import struct


def byte_length() -> int:
    return 8


def read(buf):
    data = buf.read(byte_length())
    _double = struct.unpack('>d', data)[0]

    return float(_double)
