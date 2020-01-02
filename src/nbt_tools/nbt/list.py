from nbt_tools.nbt import main as nbt

def byte_length() -> int:
    return 1

def byte_length_payload_size() -> int:
    return 4

def read(info, buf, mutdata):
    # list of type tagId (byte, int, long, string, etc)
    tagId = nbt.to_int(buf.read(byte_length()))
    listSize = buf.read(byte_length_payload_size())
    payloadSize = (listSize[0] << 24) | (listSize[1] << 16) | (listSize[2] << 8) | listSize[3]
    tags = []

    for i in range(payloadSize):
        newdata = dict()
        nbt.read_tag(buf, newdata)
        tags.append(newdata)

    return tags
