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
        for i in range(payload_size):
            tag_reader = nbt.get_tag_reader(tag_type)
            val = tag_reader(buf)

            tags.append(val)

    return {'tags': tags, 'type': tag_type.value}
