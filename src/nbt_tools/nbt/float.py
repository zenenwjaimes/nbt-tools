from nbt_tools.nbt import main as nbt
import struct

def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())
    _float = struct.unpack('>f', data)[0] #(data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    
    # TODO: use numpy if precision is required, which it is
    return float(_float)


