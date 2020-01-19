from nbt_tools.nbt import byte
from nbt_tools.nbt import main as nbt
import struct


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    values = []

    for i in range(_size):
        val = byte.read(buf)
        values.append(val)

    return {'size': _size, 'value': values, 'size_bytes': 1}

# TODO: Validate all the values passed in to make sure they're bytes
def write(data):
    arr = data['value']['value']
    packed = list(map(lambda _byte: struct.pack('>b', _byte), arr))

    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(len(data['value']['value'])).to_bytes(4, byteorder='big'),
            b''.join(packed)
    ])

    return res
