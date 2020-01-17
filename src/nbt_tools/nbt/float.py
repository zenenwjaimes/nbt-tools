import struct
from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _float = struct.unpack('>f', data)[0]

    # TODO: use numpy if precision is required, which it is
    return float(_float)


def write(data):
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            struct.pack(">f", data['value'])
    ])

    return res 
