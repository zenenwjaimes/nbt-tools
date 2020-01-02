from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 2

def read(info, buf, mutdata):
    data = buf.read(byte_length())
    _short = (data[0] << 8) | data[1]

    return _short
