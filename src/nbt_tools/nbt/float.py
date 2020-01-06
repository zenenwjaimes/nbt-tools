import struct


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _float = struct.unpack('>f', data)[0]

    # TODO: use numpy if precision is required, which it is
    return float(_float)
