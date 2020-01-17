from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return 1


def byte_length_payload_size() -> int:
    return 4


def read(buf):
    # list of type tag_id (byte, int, compound, string, etc)
    tag_type = nbt.tag_type(buf.read(byte_length()))
    list_size = buf.read(byte_length_payload_size())
    payload_size = nbt.to_int(list_size)
    tags = []

    if tag_type.value == nbt.TAG.Compound.value:
        for i in range(payload_size):
            newdata = []
            nbt.read_tag(buf, newdata)
            tags.append(newdata)
    else:
        tag_reader = nbt.get_tag_reader(tag_type)

        for i in range(payload_size):
            val = tag_reader(buf)
            tags.append(val)

    return {'value': tags, 'type': tag_type.value}


def write(data):
    list_data = data['value']
    tag_type = nbt.tag_type(list_data['type'])
    list_output = []

    if tag_type.value == nbt.TAG.Compound.value:
        pass
    else:
        tag_writer = nbt.get_tag_writer(tag_type)

        for tag in list_data['value']:
            list_output.append(tag_writer({'tag_name': '', 'value': tag}))

    res = b''.join([
            nbt.get_tag_header(data),
            bytes(data['tag_name'], 'utf-8'),
            int(data['value']['type']).to_bytes(1, byteorder='big'), #tagId
            int(len(data['value'])).to_bytes(4, byteorder='big'), #payload size
            b''.join(list_output)
    ])

    return res
