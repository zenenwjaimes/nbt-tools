from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 4


def read(buf):
    data = buf.read(byte_length())

    return nbt.to_int(data)
