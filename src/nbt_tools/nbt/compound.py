from nbt_tools.nbt import main as nbt


def byte_length() -> int:
    return -1


def read(buf):
    newdata = []
    nbt.read_tag(buf, newdata)

    return newdata


def write(data, list_type=False):
    list_data = data['value']
    list_output = []
    end_tag = nbt.get_tag_writer(nbt.tag_type(nbt.TAG.End))({})

    for tag in list_data:
        tag_type = nbt.tag_type(tag['type'])
        tag_writer = nbt.get_tag_writer(tag_type)

        list_output.append(tag_writer(tag))
   
    # TODO: Fix this hack. it's to prevent a list of compound type
    # from adding the tag header twice since the list adds tagId
    if list_type == True:
        res = b''.join([
                b''.join(list_output),
                end_tag
        ])
    else:
        res = b''.join([
                nbt.get_tag_header(data),
                bytes(data['tag_name'], 'utf-8'),
                b''.join(list_output),
                end_tag
        ])

    return res
