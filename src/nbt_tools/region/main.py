from nbt_tools.nbt import main as nbt
from nbt_tools.region import math as region_math
import collections
import io
import struct
import zlib
import math

Point = collections.namedtuple('Point', 'x y')
Chunk = collections.namedtuple('Chunk', 'x z')


def load_region(filename, debug=False):
    data = {}
    rpos = filename.find('r.')
    region = filename[rpos:].replace('r.', '').replace('.mca','').replace('.',',').split(',')

    with open(filename, 'rb') as fp:
        header_data = fp.read(8192)
        region_data = fp.read()

    data = parse_region_data(header_data, region_data, region)
    return data


def save_region(filename, nbt_data):
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)

    # write chunk location
    for loc in nbt_data['locations']:
        tree_fitty = struct.pack(">I", loc['offset'])

        buf.write(tree_fitty[-3:]) # offset
        buf.write(struct.pack('>b', loc['sectors'])) # sector count

    # write chunk timestamps
    for ts in nbt_data['timestamps']:
        buf.write(struct.pack('>i', ts['ts'])) # timestamps

    chunks = []

    # write chunk data...
    _i = io.BytesIO()
    _b = io.BufferedWriter(_i)

    # TODO: Fix this sorting issue. Chunks need to be written in a 
    # specific order.
    chunky = nbt_data['chunks']
    sorted_chunks = sorted(chunky, key=lambda x: x['offset'])

    for chunk_data in sorted_chunks:
        if len(chunk_data['chunk']) > 0:
            chunk_nbt = nbt.write_tag(_b, chunk_data['chunk'])
        else:
            chunk_nbt = b''

        b_len = struct.pack('>I', chunk_data['length'])
        b_comp = struct.pack('>B', chunk_data['compression'])
        b_data = zlib.compress(chunk_nbt)

        b_enc = b''.join([b_len, b_comp, b_data])

        chunks.append(b_enc)

        padding = (math.ceil(len(b_enc)/4096)*4096) - len(b_enc)
        chunks.append(b'\x00' * padding)

    _chunk_bytes = b''.join(chunks)
    _i.close()
    _b.close()

    buf.write(_chunk_bytes)
    #print('CHUNK LEN IS {} needs padding of {}'.format(len(_chunk_bytes), padding))
    #buf.write(b'\x00' * padding)
    buf.seek(0)

    dest_path = 'heckle_1'

    with open(dest_path, 'wb') as f:
        f.write(bio.read())


def parse_region_data(header, region_data, region):
    chunks = []
    locations = []
    timestamps = []

    reg_x = int(region[0]) * 32
    reg_z = int(region[1]) * 32

    location_tuples = [
            Chunk(x, z)
            for x in range(reg_x, reg_x + 32)
            for z in range(reg_z, reg_z + 32)
    ]

    temp_header = bytes(header[0:8192])
    temp_chunk_data = bytes(region_data)

    for coords in location_tuples:
        chunk = Chunk._make(coords)

        chunk_loc_data = get_location_data(temp_header[0:4096], chunk)
        chunk_ts_data = get_timestamp_data(temp_header[4096:8192], chunk)

        locations.append(chunk_loc_data)
        timestamps.append(chunk_ts_data)

        print(chunk_loc_data)

        chunks.append(get_chunk_data(
                temp_chunk_data,
                chunk,
                {'loc': chunk_loc_data, 'ts': chunk_ts_data}
        ))

    res = {'locations': locations, 'timestamps': timestamps, 'chunks': chunks}

    return res

def get_chunk_data(region_data, chunk, info):
    # max chunk size 1MB, each sector being 4KB, max sectors is 256
    fixed_offset = loc_offset = info['loc']['offset'] * 4096
    sectors = info['loc']['sectors']

    # lop off the first 8K for the header from the offset
    # which is included in this field
    if info['loc']['offset'] > 0:
        loc_offset -= 8192
    else:
        return {
            'data': b'',
            'chunk': [],
            'unc': b'',
            'x': chunk.x,
            'z': chunk.z,
            'length': 0,
            'offset': info['loc']['offset'],
            'compression': 0
        }
    print('INITIAL LOC: {}'.format(loc_offset))
    #loc_offset = ((loc_offset >> 8) * 4096)

    print('LOC {}'.format(loc_offset))

    b0 = region_data[loc_offset+0]
    b1 = region_data[loc_offset+1]
    b2 = region_data[loc_offset+2]
    b3 = region_data[loc_offset+3]
    compression_type = region_data[loc_offset+4]
    loc_offset += 5

    length = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3
    print('LENGTH IS {} of ({}, {})'.format((length) - 1, chunk.x, chunk.z))
    loc_offset_end = loc_offset + (sectors * 4096) - 5

    compressed_data = region_data[loc_offset:loc_offset_end]

    print('loc offset is {} with end offset {} for x {} z {} offset {}'.format(loc_offset + 8192, loc_offset_end + 8192, chunk.x, chunk.z, info['loc']['offset']))

    chunk_data = zlib.decompress(compressed_data)

    chunky = nbt.read_nbt_bytes(chunk_data)

    xPos = nbt.get_tag_node(['root', 'xPos'], chunky)
    zPos = nbt.get_tag_node(['root', 'zPos'], chunky)

    return {
            'data': chunk_data,
            'unc': compressed_data,
            'chunk': chunky,
            'x': xPos,
            'z': zPos,
            'length': length,
            'sectors': sectors,
            'offset': fixed_offset,
            'compression': compression_type
    }


def get_timestamp_data(header, chunk):
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

    return {'ts': _int, 'x': chunk.x, 'z': chunk.z}


def get_location_data(header, chunk):
    print(chunk)
    int_offset =  ((chunk.x & 0x1f) + (chunk.z & 0x1f) * 32)  * 4 #region_math.get_chunk_location(chunk.x, chunk.z)

    b0 = header[int_offset+0]
    b1 = header[int_offset+1]
    b2 = header[int_offset+2]
    b3 = header[int_offset+3]

    _int = (b0 << 16) | (b1 << 8) | b2

    location_offset = _int
    sector_count = b3

    return {
            'offset': location_offset,
            'sectors': sector_count,
            'int_offset': int_offset,
            'x': chunk.x,
            'z': chunk.z
    }
