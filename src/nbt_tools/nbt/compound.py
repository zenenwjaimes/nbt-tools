from nbt_tools.nbt import main as nbt
import pprint

def byte_length() -> int:
    return -1

def read(info, buf, mutdata):
    newdata = dict()
    nbt.read_tag(buf, newdata)

    return newdata

