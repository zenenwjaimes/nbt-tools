import pprint
import gzip
import importlib
import io
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

def to_int(byte):
    return int(byte.hex(), 16)


def read_nbt_bytes(byte_data):
    data = dict()
    with io.BytesIO(byte_data) as fp:
        read_tag(fp, data)

    return data

def read_nbt_file(filename: str):
    data = dict()
    with open(filename, 'rb') as fp:
        read_tag(fp, data)

    return data


def unpack_nbt_file(filename: str, fn = gzip.open):
    data = dict()

    with fn(filename, 'rb') as fp:
        read_tag(fp, data)

    return data


def tag_type(_type) -> str:
    _tag_type = _type if _type != b'' else b'\x00'
    return TAG(to_int(_tag_type))


def tag_name(buf) -> str:
    length_big_byte = to_int(buf.read(1)) << 8

    # eof
    if length_big_byte == b'':
        return 

    length_small_byte = to_int(buf.read(1))

    length = length_big_byte | length_small_byte
    tag_name = buf.read(length) if length > 0 else b'root'

    return tag_name.decode("utf-8")

def tag_data(tag, buf, skip_read = False) -> dict:
    if tag == TAG.End:
        return dict({'name': 'end', 'tag': TAG.End, 'fn': 'end'})

    name = ""
        
    if skip_read == False:
        name = tag_name(buf) if tag.value != TAG.End.value else ''

    fn = tag.name.lower()
   
    return dict({'name': name, 'tag': tag, 'fn': fn})


def read_tag(buf, mutdata, typed = False):
    if typed == False:
        _type = buf.read(1)
        tag = tag_type(_type) 
    else:
        tag = TAG(typed)

    # eof
    if tag == TAG.End: #and _type != b'\x00':
        return

    data = tag_data(tag, buf, typed)

    if data['name'] != 'end':
        mod = nbt_module(data['fn'])
        tag_reader = getattr(mod, 'read')
        mutdata[data['name']] = dict({'type': tag.value, 'value': tag_reader(data, buf, mutdata)})
    if typed == False:
        read_tag(buf, mutdata, typed)


def nbt_module(fn):
    return importlib.import_module('nbt_tools.nbt.{0}'.format(fn))
