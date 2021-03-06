from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 1


def read(buf):
    data = buf.read(byte_length())

    return nbt.to_byte(data)


def write(data):
    tag_header = nbt.get_tag_header(data)
    res = b''.join([
            tag_header,
            bytes(data['tag_name'], 'utf-8'),
            int(
                data['value']).to_bytes(
                    byte_length(),
                    byteorder='big',
                    signed=True
                )
    ])

    return res
