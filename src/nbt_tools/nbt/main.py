import pprint
import gzip
import importlib
import io
import struct
from enum import Enum
from nbt_tools.nbt import * 

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
    #return int.from_bytes(byte, byteorder = 'big', signed = True)
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


def unpack_nbt_file(filename: str, fn = gzip.open):
    data = [] 

    with fn(filename, 'rb') as fp:
        read_tag(fp, data)

    return data


def pretty_print_nbt_data(nbt_data, indent = 1):
    if 'root' in nbt_data:
        pretty_print_nbt_data(nbt_data['root'], indent + 1)
    else:
        if 'type' in nbt_data and nbt_data['type'] in [TAG.Byte_Array.value, TAG.Int_Array.value, TAG.Long_Array.value, TAG.Compound.value, TAG.Compound.List]:
            for tag in nbt_data['value']:
                if 'tags' not in nbt_data['value']:
                    data = nbt_data['value'][tag]
                else:
                    data = nbt_data['value']['tags']

                pretty_print_nbt_data(data, indent)
        else:
            name = nbt_data['tag_name'] if 'tag_name' in nbt_data else 'unknown'
            print(name)
            _type = nbt_data['type']
            print('{} -> {} name={}'.format(indent * "\t", TAG(_type).name, name))


def tag_type(_type) -> str:
    _tag_type = _type if _type != b'' else b'\x00'
    return TAG(to_byte(_tag_type))


def tag_name(buf) -> str:
    length_big_byte = to_byte(buf.read(1)) << 8
    length_small_byte = to_byte(buf.read(1))

    length = length_big_byte | length_small_byte
    tag_name = buf.read(length) if length > 0 else b'root'

    return tag_name.decode("utf-8")

def tag_data(tag, buf, skip_read = False) -> dict:
    if tag == TAG.End:
        return dict({'name': 'end', 'tag': TAG.End, 'fn': 'end'})

    name = tag_name(buf) if tag.value != TAG.End.value else ''
    fn = tag.name.lower()
   
    return dict({'name': name, 'tag': tag, 'fn': fn})


def read_tag(buf, mutdata):
    #print('FP is at {}'.format(buf.tell()))
    _type = buf.read(1)
    tag = tag_type(_type) 
    
    # eof
    if tag == TAG.End: #and _type != b'\x00':
        return

    data = tag_data(tag, buf)

    if data['name'] != 'end':
        tag_reader = get_tag_reader(tag)
        val = tag_reader(buf)
        mutdata.append({'tag_name': data['name'], 'tag': tag, 'type': tag.value, 'value': val})

    read_tag(buf, mutdata)


def get_tag_reader(tag):
    mod = get_nbt_fn(tag.name.lower())
    return getattr(mod, 'read')


def get_nbt_fn(fn):
    return importlib.import_module('nbt_tools.nbt.{0}'.format(fn))
