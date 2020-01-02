from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 8


def read(info, buf, mutdata):
    data = buf.read(byte_length())
    _long = (data[0] << 56) | (data[1] << 48) | (data[2] << 40) | (data[3] << 32) | (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]

    return _long


