from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 2


def read(buf):
    data = buf.read(byte_length())
    length = (data[0] << 8) | data[1]
    string = buf.read(length).decode("utf-8")

    return string


def write(data):
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(len(data['value'])).to_bytes(byte_length(), byteorder='big'),
            bytes(data['value'], 'utf-8')
    ])

    return res
