from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 4

def read(buf):
    data = buf.read(byte_length())
    _int = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    return _int


