from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return -1


def read(buf):
    newdata = []
    nbt.read_tag(buf, newdata)

    return newdata
