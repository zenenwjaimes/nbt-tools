from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 4

def read(info, buf, mutdata):
    data = buf.read(byte_length())
    _byte_size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    fresh_bytes = buf.read(_byte_size)

    return dict({'size': _byte_size, 'raw': fresh_bytes, 'value': _byte_size})
