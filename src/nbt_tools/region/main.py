from nbt_tools.nbt import main as nbt
from nbt_tools.region import math as region_math
import collections

import pprint

Point = collections.namedtuple('Point', 'x y')
Chunk = collections.namedtuple('Chunk', 'x z')

def load_region(filename, debug = False):
    header = {}
    chunks = {}
    data = {}

    with open(filename, 'rb') as fp:
        header_data = fp.read(8192)

    data = parse_header(header_data)

    #nbt_data = nbt.unpack_nbt_data(filename)

    if debug:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(header)
        print(filename)

    return data


def parse_header(header):
    chunks = {}
    locations = []
    timestamps = []
    
    location_tuples = [Chunk(x, z) for x in range(16)
                             for z in range(16)]

    temp_header = bytes(header[0:4096])

    for coords in location_tuples:
        chunk = Chunk._make(coords)
        locations.append(get_location_data(temp_header, chunk))
        timestamps.append(get_timestamp_data(temp_header, chunk))

    return {'locations': locations, 'timestamps': timestamps, 'chunks': chunks}


def get_chunk_data(region_data, chunk):

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 25) | (b1 << 16) | (b2 << 8) | b3

    return {'ts': _int, 'x': chunk.x, 'z': chunk.z}


def get_timestamp_data(header, chunk):
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)
    print('len {0} for {1},{2}, offset is {3}'.format(len(header),chunk.x,chunk.z,int_offset))

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 25) | (b1 << 16) | (b2 << 8) | b3

    return {'ts': _int, 'x': chunk.x, 'z': chunk.z}


def get_location_data(header, chunk):
    print(region_math)
    print(chunk)
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)
    print('len {0} for {1},{2}, offset is {3}'.format(len(header),chunk.x,chunk.z,int_offset))

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 16) | (b1 << 8) | b2

    location_offset = _int
    sector_count = b3

    return {'offset': location_offset, 'sectors': sector_count, 'x': chunk.x, 'z': chunk.z}
