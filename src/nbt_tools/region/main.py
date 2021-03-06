from nbt_tools.nbt import main as nbt
from nbt_tools.region import math as region_math
import collections
import io
import struct
import zlib
import math
import numpy as np

Point = collections.namedtuple('Point', 'x y')
Chunk = collections.namedtuple('Chunk', 'x z')


def filename_to_region_coords(filename):
    rpos = filename.find('r.')
    region = (
                filename[rpos:]
                .replace('r.', '')
                .replace('.mca', '')
                .replace('.old', '')
                .replace('.end', '')
                .replace('.nether', '')
                .replace('.', ',')
                .split(',')
            )

    return Chunk(region[0], region[1])


def load_region(filename, debug=False):
    data = {}
    region = filename_to_region_coords(filename)

    with open(filename, 'rb') as fp:
        header_data = fp.read(8192)
        region_data = fp.read()

    data = parse_region_data(header_data, region_data, region)
    return data


def save_region(dest_path, filename, nbt_data):
    region = filename_to_region_coords(filename)
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)

    # write chunk location
    header = []
    for loc in nbt_data['locations']:
        tree_fitty = struct.pack(">I", loc['offset'])
        offset = tree_fitty[-3:]
        sectors = struct.pack('>b', loc['sectors'])

        header.append(offset)
        header.append(sectors)

    buf.write(b''.join(header))

    # write chunk timestamps
    timestamps = []
    for ts in nbt_data['timestamps']:
        timestamps.append(struct.pack('>i', ts['ts']))

    buf.write(b''.join(timestamps))

    for chunk_data in nbt_data['chunks']:
        # write chunk data...
        _i = io.BytesIO()
        _b = io.BufferedWriter(_i)

        b_data = b''

        if len(chunk_data['chunk']) > 0:
            chunk_nbt = nbt.write_tag(_b, chunk_data['chunk'])
            b_data = zlib.compress(chunk_nbt)

        b_len = struct.pack('>i', len(b_data))
        b_comp = struct.pack('>b', chunk_data['compression'])
        b_enc = b''.join([b_len, b_comp, b_data])

        buf.seek(chunk_data['offset'])
        buf.write(b_enc)

        _i.close()
        _b.close()

    buf.seek(0)
    buf.flush()

    res = bio.read()

    # TODO: Fix this hack. There's a problem with going over
    padding = (math.ceil(len(res)/4096)*4096) - len(res)
    buf.write(b'\x00' * padding)

    f = open('{}/r.{}.{}.mca'.format(dest_path, region.x, region.z), 'wb')
    f.write(res)
    f.close()

    bio.close()
    buf.close()


def relocate_region(offset, nbt_data):
    coord_offset = region_math.region_to_coord(*offset)

    for chunk in nbt_data['chunks']:
        if len(chunk['chunk']) == 0:
            continue

        entities = nbt.get_tag_node(['', 'Level', 'Entities'], chunk['chunk'])
        if entities is not False:
            #entities['value']['value'] = []
            for entity in entities['value']['value']:
                pos = nbt.get_tag_node(['Pos'], entity) 

                if pos is not False:
                    pos_list = pos['value']['value']
                    pos_list[0] += coord_offset[0]
                    pos_list[2] += coord_offset[1]
                    pos['value']['value'] = pos_list

        tile_entities = nbt.get_tag_node(['', 'Level', 'TileEntities'], chunk['chunk'])
        if tile_entities is not False:
            for tile_entity in tile_entities['value']['value']:
                x_pos = nbt.get_tag_node(['x'], tile_entity)
                z_pos = nbt.get_tag_node(['z'], tile_entity)

                x_pos['value'] += coord_offset[0]
                z_pos['value'] += coord_offset[1]

        structures = nbt.get_tag_node(
                ['', 'Level', 'Structures', 'Starts'],
                chunk['chunk']
        )
        references = nbt.get_tag_node(
                ['', 'Level', 'Structures', 'References'],
                chunk['chunk']
        )

        if references is not False:
            for reference in references['value']:
                fixed = []

                for struct_ref in reference['value']['value']:
                    struct_ref_x = np.int32(struct_ref & 0xffffffff)
                    struct_ref_z = np.int32((struct_ref >> 32) & 0xffffffff)
                    
                    struct_ref_x += offset[0] * 32
                    struct_ref_z += offset[1] * 32

                    mut_ref = np.int64((struct_ref_z << 32) | struct_ref_x)
                    fixed.append(np.int64(mut_ref))

                reference['value']['value'] = tuple(fixed)

        if structures is not False:
            for structure in structures['value']:
                struct_id = nbt.get_tag_node(['id'], structure['value'])
                x_pos = nbt.get_tag_node(['ChunkX'], structure['value'])
                z_pos = nbt.get_tag_node(['ChunkZ'], structure['value'])
                bb_pos = nbt.get_tag_node(['BB'], structure['value'])
                struct_children = nbt.get_tag_node(
                        ['Children'],
                        structure['value']
                )

                if struct_id['value'] != 'INVALID':
                    x_pos['value'] += offset[0] * 32
                    z_pos['value'] += offset[1] * 32

                if bb_pos is not False:
                    bb_positions = bb_pos['value']['value']
                    # bounding box min x, z
                    bb_positions[0] += coord_offset[0]
                    bb_positions[2] += coord_offset[1]
                    # bounding box max x, z
                    bb_positions[3] += coord_offset[0]
                    bb_positions[5] += coord_offset[1]

                if struct_children is not False:
                    for struct_child in struct_children['value']['value']:
                        struct_bb = nbt.get_tag_node(['BB'], struct_child)
                        entrances = nbt.get_tag_node(
                                ['Entrances'],
                                struct_child
                        )

                        if struct_bb is not False:
                            struct_bb_pos = struct_bb['value']['value']
                            # bounding box min x, z
                            struct_bb_pos[0] += coord_offset[0]
                            struct_bb_pos[2] += coord_offset[1]
                            # bounding box max x, z
                            struct_bb_pos[3] += coord_offset[0]
                            struct_bb_pos[5] += coord_offset[1]
                        if entrances is not False:
                            for entrance in entrances['value']['value']:
                                entrance['value'][0] += coord_offset[0]
                                entrance['value'][2] += coord_offset[1]
                                entrance['value'][3] += coord_offset[0]
                                entrance['value'][5] += coord_offset[1]

        # move chunks to new offset 
        x_pos = nbt.get_tag_node(['', 'Level', 'xPos'], chunk['chunk'])
        z_pos = nbt.get_tag_node(['', 'Level', 'zPos'], chunk['chunk'])
        x_pos['value'] += offset[0] * 32
        z_pos['value'] += offset[1] * 32

        structures = nbt.get_tag_node(['', 'Level', 'Structures', 'Starts'], chunk['chunk'])

def parse_region_data(header, region_data, region):
    chunks = []
    locations = []
    timestamps = []

    reg_x = int(region.x) * 32
    reg_z = int(region.z) * 32

    location_tuples = [
            Chunk(x, z)
            for z in range(reg_z, reg_z + 32)
            for x in range(reg_x, reg_x + 32)
    ]

    temp_header = bytes(header[0:8192])
    temp_chunk_data = bytes(region_data)
    total_size = 8192  # at least header present

    for coords in location_tuples:
        chunk = Chunk._make(coords)

        chunk_loc_data = get_location_data(temp_header[0:4096], chunk)
        chunk_ts_data = get_timestamp_data(temp_header[4096:8192], chunk)

        locations.append(chunk_loc_data)
        timestamps.append(chunk_ts_data)

        chunk_data = get_chunk_data(
                temp_chunk_data,
                chunk,
                {'loc': chunk_loc_data, 'ts': chunk_ts_data}
        )

        total_size += chunk_data['sectors'] * 4096
        chunks.append(chunk_data)

    res = {
            'locations': locations,
            'timestamps': timestamps,
            'chunks': chunks,
            'approx_size': total_size
    }

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
            'x': chunk.x,
            'z': chunk.z,
            'length': 0,
            'sectors': 0,
            'offset': fixed_offset,
            'compression': 0
        }

    b0 = region_data[loc_offset+0]
    b1 = region_data[loc_offset+1]
    b2 = region_data[loc_offset+2]
    b3 = region_data[loc_offset+3]
    compression_type = region_data[loc_offset+4]
    loc_offset += 5

    length = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3
    loc_offset_end = loc_offset + (sectors * 4096) - 5

    compressed_data = region_data[loc_offset:loc_offset_end]
    chunk_data = zlib.decompress(compressed_data)
    chunky = nbt.read_nbt_bytes(chunk_data)

    xPos = nbt.get_tag_node(['', 'Level', 'xPos'], chunky)
    zPos = nbt.get_tag_node(['', 'Level', 'zPos'], chunky)

    return {
            'data': b'',  # chunk_data,
            'chunk': chunky,
            'x': xPos['value'],
            'z': zPos['value'],
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
    int_offset = region_math.get_chunk_location(chunk.x, chunk.z)

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
