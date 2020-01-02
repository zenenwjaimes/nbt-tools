from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 4


def read(info, buf, mutdata):
    data = buf.read(byte_length())
    _float = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    
    # TODO: use numpy if precision is required, which it is
    return float(_float)

