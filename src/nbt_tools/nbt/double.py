import struct
from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 8


def read(buf):
    data = buf.read(byte_length())
    _double = struct.unpack('>d', data)[0]

    return float(_double)


def write(data):
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            struct.pack('d', data['value'])
    ])

    return res 
