from nbt_tools.nbt import long
from nbt_tools.nbt import main as nbt
import struct


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    values = []
    ready = buf.read(_size * 8)

    if _size > 1:
        values = nbt.to_long(ready, _size)
    elif _size == 1:
        values = [nbt.to_long(ready, _size)]
    else:
        values = []

    return {'size': _size, 'value': values, 'size_bytes': 8}


# TODO: Validate all the values passed in to make sure they're longs
def write(data):
    arr = data['value']['value']
    try:
        packed = nbt.to_byte_long(arr, len(arr))
    except:
        print(arr)
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            # payload size
            int(len(data['value']['value'])).to_bytes(4, byteorder='big'),
            packed
    ])

    return res
