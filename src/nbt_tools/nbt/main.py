import gzip
import importlib
import io
import struct
from enum import Enum

"""
TAG Format

0: TAG id
1-2: Tag Name Length
3-x: Tag Name
x-: Tag Data 

"""

class TAG(Enum):
    End = 0x0
    Byte = 0x1
    Short = 0x2
    Int = 0x3
    Long = 0x4
    Float = 0x5
    Double = 0x6
    Byte_Array = 0x7
    String = 0x8
    List = 0x9
    Compound = 0xA
    Int_Array = 0xB
    Long_Array = 0xC


def to_byte(byte):
    return struct.unpack('>b', byte)[0]


def to_short(byte):
    return struct.unpack('>h', byte)[0]


def to_int(byte):
    return struct.unpack('>i', byte)[0]


def to_long(byte):
    return struct.unpack('>q', byte)[0]


def read_nbt_bytes(byte_data):
    data = []

    with io.BytesIO(byte_data) as fp:
        read_tag(fp, data)

    return data


def read_nbt_file(filename: str):
    data = []

    with open(filename, 'rb') as fp:
        read_tag(fp, data)

    return data


def unpack_nbt_file(filename: str, fn=gzip.open):
    data = []

    with fn(filename, 'rb') as fp:
        read_tag(fp, data)

    return data


def pretty_print(indent, tag, name, val={}):
    print('{} -> {} name={} value={}'.format(
            indent * "\t",
            tag['tag'].name,
            name,
            val
        )
    )


def pretty_print_nbt_data(nbt_data, indent=0):
    if type(nbt_data) is list:
        for tag in nbt_data:
            if type(tag) is list:
                print('{} ->'.format('\t' * indent))

                pretty_print_nbt_data(tag, indent + 1)
            elif type(tag) is dict:
                val = tag['value']

                if type(val) is list:
                    print('{} -> {} -> name={}'.format(
                        '\t' * indent,
                        tag['tag'].name,
                        tag['tag_name']
                    ))
                    pretty_print_nbt_data(val, indent + 1)
                else:
                    if type(tag['value']) is dict:
                        print('{} -> {} -> name={}'.format(
                            '\t' * indent,
                            tag['tag'].name,
                            tag['tag_name']
                        ))

                        if type(tag['value']) is list:
                            pretty_print_nbt_data([tag['value']], indent + 1)
                        else:
                            pretty_print_nbt_data(tag, indent + 1)
                    else:
                        print('{} -> {} -> name={} value={}'.format(
                            '\t' * indent,
                            tag['tag'].name,
                            tag['tag_name'],
                            tag['value']
                        ))
            else:
                print('{} -> {}'.format('\t' * indent, tag))
    else:
        pretty_print_nbt_data(nbt_data['value'], indent + 1)


def tag_type(_type) -> str:
    _tag_type = _type if _type != b'' else b'\x00'
    return TAG(to_byte(_tag_type) if type(_tag_type) is bytes else _tag_type)


def tag_name(buf) -> str:
    length_big_byte = to_byte(buf.read(1)) << 8
    length_small_byte = to_byte(buf.read(1))

    length = length_big_byte | length_small_byte
    tag_name = buf.read(length) if length > 0 else b''

    return tag_name.decode("utf-8")


def tag_data(tag, buf, skip_read=False):
    if tag == TAG.End:
        return {'name': 'end', 'tag': TAG.End, 'fn': 'end'}

    name = tag_name(buf) if tag.value != TAG.End.value else ''
    fn = tag.name.lower()

    return {'name': name, 'tag': tag, 'fn': fn}


def read_tag(buf, mutdata, only_once=False):
    _type = buf.read(1)
    tag = tag_type(_type)

    # eof
    if tag == TAG.End:
        return

    data = tag_data(tag, buf)

    if data['name'] != 'end':
        tag_reader = get_tag_reader(tag)
        val = tag_reader(buf)

        mutdata.append({
            'tag_name': data['name'],
            #'tag': tag,
            'type': tag.value,
            'value': val
        })

    if only_once is False:
        read_tag(buf, mutdata)


def write_tag(buf, data):
    _type = data['type']
    tag = tag_type(_type)

    tag_writer = get_tag_writer(tag)
    res = tag_writer(data)
    buf.write(res)

    return res


def get_tag_header(data):
    # avoid passing header data for list tag types
    if 'type' not in data:
        return b''

    return b''.join([
        int(data['type']).to_bytes(1, byteorder='big'),
        int(len(data['tag_name'])).to_bytes(2, byteorder='big')
    ])


def get_tag_reader(tag):
    mod = get_nbt_fn(tag.name.lower())
    return getattr(mod, 'read')


def get_tag_writer(tag):
    mod = get_nbt_fn(tag.name.lower())
    return getattr(mod, 'write')


def get_nbt_fn(fn):
    return importlib.import_module('nbt_tools.nbt.{0}'.format(fn))


def get_tag_node(path, nbt_data):
    curr_path = path[0:1]

    if type(nbt_data) is list:
        for tag in nbt_data:
            if curr_path[0] == tag['tag_name']:
                if (len(path) > 1):
                    return get_tag_node(path[1:], tag['value'])
                else:
                    return tag
        return False
