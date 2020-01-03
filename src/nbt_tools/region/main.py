from nbt_tools.nbt import main as nbt
from nbt_tools.region import math as region_math
import collections
import pprint
import zlib

Point = collections.namedtuple('Point', 'x y')
Chunk = collections.namedtuple('Chunk', 'x z')

def load_region(filename, debug = False):
    header = {}
    chunks = {}
    data = {}

    with open(filename, 'rb') as fp:
        header_data = fp.read(8192)
        region_data = fp.read()

    data = parse_region_data(header_data, region_data)

    return data


def parse_region_data(header, region_data):
    chunks = {}
    locations = []
    timestamps = []
    
    location_tuples = [Chunk(x, z) for x in range(16)
                             for z in range(16)]

    temp_header = bytes(header[0:4096])
    temp_chunk_data = bytes(region_data)

    for coords in location_tuples:
        chunk = Chunk._make(coords)

        chunk_loc_data = get_location_data(temp_header, chunk)
        chunk_ts_data = get_timestamp_data(temp_header, chunk)

        locations.append(chunk_loc_data)
        timestamps.append(chunk_ts_data)
        chunks[chunk] = get_chunk_data(temp_chunk_data, chunk, {'loc': chunk_loc_data, 'ts': chunk_ts_data})

    return {'locations': locations, 'timestamps': timestamps, 'chunks': chunks}


def get_chunk_data(region_data, chunk, info):
    int_offset = info['loc']['offset'] 
    # max chunk size 1MB, each sector being 4KB, max sectors is 256  
    sector_offset = info['loc']['sectors'] * 4096 

    b0 = region_data[sector_offset+0]
    b1 = region_data[sector_offset+1]
    b2 = region_data[sector_offset+2]
    b3 = region_data[sector_offset+3]
    compression_type = region_data[sector_offset+4]

    length = (b0 << 25) | (b1 << 16) | (b2 << 8) | b3
    compressed_data = region_data[sector_offset+5:]
    chunk_data = zlib.decompress(compressed_data[0:length])

    chunky = nbt.read_nbt_bytes(chunk_data)

    return {'data': chunk_data, 'chunk': chunky, 'x': chunk.x, 'z': chunk.z, 'length': length, 'compression': compression_type}


def get_timestamp_data(header, chunk):
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 25) | (b1 << 16) | (b2 << 8) | b3

    return {'ts': _int, 'x': chunk.x, 'z': chunk.z}


def get_location_data(header, chunk):
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 16) | (b1 << 8) | b2

    location_offset = _int
    sector_count = b3

    return {'offset': location_offset, 'sectors': sector_count, 'x': chunk.x, 'z': chunk.z}
