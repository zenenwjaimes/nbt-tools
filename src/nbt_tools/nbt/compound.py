from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return -1


def read(buf):
    newdata = []
    nbt.read_tag(buf, newdata)

    return newdata


def write(data):
    list_data = data['value']
    tag_type = nbt.tag_type(list_data['type'])
    list_output = []

    tag_writer = nbt.get_tag_writer(tag_type)

    for tag in list_data['value']:
        list_output.append(tag_writer(tag))

    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            b''.join(list_output)
    ])

    return res
