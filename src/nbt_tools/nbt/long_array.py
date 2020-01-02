from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 4

def read(info, buf, mutdata):
    data = buf.read(byte_length())
    _size = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    tags = []
    for i in range(_size):
        newdata = dict()
        nbt.read_tag(buf, newdata, nbt.TAG.Long.value)
        tags.append(newdata)

    values = list(map(lambda tag: tag['']['value'], tags))

    return dict({'size': _size, 'raw': values, 'value': _size, 'size_bytes': 8, 'tags': tags})
