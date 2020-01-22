from nbt_tools.nbt import long
from nbt_tools.nbt import main as nbt
import struct


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    values = []

    for i in range(_size):
        val = long.read(buf)
        values.append(val)

    return {'size': _size, 'value': values, 'size_bytes': 8}


# TODO: Validate all the values passed in to make sure they're longs
def write(data):
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            # payload size
            int(len(data['value']['value'])).to_bytes(4, byteorder='big'),
            b''.join(longs_to_bytes(data['value']['value']))
    ])

    return res


def longs_to_bytes(vals):
    return list(map(lambda val: struct.pack('>q', val), vals))
