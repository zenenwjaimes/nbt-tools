from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 4

def read(buf):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    values = []

    for i in range(_size):
        val = byte.read(buf)
        values.append(val)

    return {'size': _size, 'raw': values, 'value': _size, 'size_bytes': 4}
