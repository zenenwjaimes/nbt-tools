from nbt_tools.nbt import byte
from nbt_tools.nbt import main as nbt
import struct


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    values = []
    ready = buf.read(_size)

    if _size > 1:
        values = nbt.to_byte(ready, _size)
    elif _size == 1:
        values = [nbt.to_byte(ready, _size)]
    else:
        values = []


    return {'size': _size, 'value': list(values), 'size_bytes': 1}


# TODO: Validate all the values passed in to make sure they're bytes
def write(data):
    arr = data['value']['value']
    packed = nbt.to_byte_byte(arr, len(arr))

    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(len(data['value']['value'])).to_bytes(4, byteorder='big'),
            packed
    ])

    return res
