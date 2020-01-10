from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 1


def read(buf):
    data = buf.read(byte_length())

    return nbt.to_byte(data)

def write(data):
    tag_header = nbt.get_tag_header(data)
    #print(data)
    #print(int(data['value']).to_bytes(1, byteorder='big'))
    print('tag header {}'.format(tag_header))
    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(data['value']).to_bytes(1, byteorder='big')
    ])
    print('res {}'.format(res))

    return res 
