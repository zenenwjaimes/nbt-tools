from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 2


def read(buf):
    data = buf.read(byte_length())

    return nbt.to_short(data)


def write(data):
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(data['value']).to_bytes(
                    byte_length(),
                    byteorder='big',
                    signed=True
            )
    ])

    return res
