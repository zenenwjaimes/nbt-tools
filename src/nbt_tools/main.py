
# -*- coding: utf-8 -*-
"""
Simple utility to relocate region files from [x1,y1 x2,y2] to x3,y3
offset from 0,0
"""

import argparse
import io
import sys
import traceback
import logging
import shutil
import os.path
import os
import fnmatch
import gzip
import numpy
import json

from multiprocessing import Pool
from os import path
from nbt_tools import __version__
from nbt_tools.region import math
from nbt_tools.nbt import main as nbt
from nbt_tools.mcfiles import main as maps
from nbt_tools.region import main as region
from nbt_tools.region import math as region_math

__author__ = "zenen jaimes"
__copyright__ = "zenen jaimes"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def calculate_regions(coord_range, offset_coord, from_path, to_path):
    offset_x = offset_coord[0]
    offset_z = offset_coord[1]
    offset = math.coord_offset(offset_x, offset_z)

    min_bound = math.coord_to_region(coord_range[0], coord_range[1])
    max_bound = math.coord_to_region(coord_range[2], coord_range[3])

    regions = math.regions_for_range(
                min_bound[0],
                min_bound[1],
                max_bound[0],
                max_bound[1]
    )
    mappings = tuple(math.region_mappings(regions, offset))
    args = []
    l = numpy.array_split(mappings, 8)
    for region in l:
        args.append(
                {
                    'offset': (offset_x, offset_z),
                    'from_path': from_path,
                    'to_path': to_path,
                    'regions': region
                }
        )

    p = Pool(8)
    p.map(pool_output_regions, args)
    #[output_region_cmd(
    #    region,
    #    (offset_x, offset_z),
    #    from_path,
    #    to_path
    #) for region in mappings]


def pool_output_regions(data):
    [output_region_cmd(
        region,
        data['offset'],
        data['from_path'],
        data['to_path']
    ) for region in data['regions']]


def output_region_cmd(reg, offset, from_path, to_path):
    offset = math.coord_to_region(offset[0], offset[1])
    from_xy = reg[0]
    to_xy = reg[1]

    src_region_file = 'r.{0}.{1}.mca'.format(*from_xy)
    src_full_file = '{0}/{1}'.format(from_path, src_region_file)

    dest_region_file = 'r.{0}.{1}.mca'.format(*to_xy)
    dest_full_file = '{0}/{1}'.format(to_path, dest_region_file)

    if (path.isfile(src_full_file)):
        try:
            nbt_data = region.load_region(src_full_file)
            region.relocate_region(offset, nbt_data)
            region.save_region(to_path, dest_region_file, nbt_data)

            print('Copied "{0}" to "{1}"\n'.format(
                src_region_file,
                dest_region_file
            ))
            ""
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)))
            msg = 'Source doesn\'t exist. Failed to copy "{0}" to "{1}"\n'

            print(msg.format(
                src_region_file,
                dest_region_file
            ))

    else:
        print('Region File Doesn\'t Exist "{0}" to "{1}"\n'.format(
            src_full_file,
            dest_full_file
        ))

        #nbt_data = region.load_region(src_full_file)
        #region.relocate_region(offset, nbt_data)
        #region.save_region(to_path, dest_region_file, nbt_data)


def parse_args(args):
    """Parse command line parameters
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="NBT File Manipulation")

    parser.add_argument(
        '--loglevel',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default="INFO"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="nbt_tools {ver}".format(ver=__version__)
    )
    parser.add_argument(
        '--src-path',
        help='Src path for file(s)',
        required=True
    )
    help_msg = 'Use this option for region files,' \
        ' or nbt files that aren\'t gzipped'
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--unpacked-nbt', action='store_true', help=help_msg)
    group.add_argument('--nbt', action='store_true')
    group.add_argument('--json-dump', action='store_true')
    group.add_argument('--json-load', action='store_true')
    group.add_argument('--gen-nbt', action='store_true')
    group.add_argument('--chunk-relocator', action='store_true')
    group.add_argument('--map-gen', action='store_true')
    group.add_argument('--region', action='store_true')
    map_group = parser.add_argument_group(
            'Map to Image Generator',
            'Image files will be generated from all the map_*.dat files'
    )
    map_group.add_argument(
        '--output-dir',
        help='dir path of where map images will be saved',
        default="./maps"
    )

    chunk_relocator_group = parser.add_argument_group(
        'Chunk Relocator',
        'Move chunk files from one save to another with an x,z offset'
    )
    chunk_relocator_group.add_argument(
        '--point1',
        help='(x,z) of one corner'
    )
    chunk_relocator_group.add_argument(
        '--point2',
        help='(x,z) of opposite corner'
    )
    chunk_relocator_group.add_argument(
        '--dest-point',
        help='(x,z) where to move your map relative to (0,0)'
    )
    chunk_relocator_group.add_argument(
        '--dest-path',
        help='Dest path for nbt file(s)'
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def map_generator(args):
    """Map Generator from map_X.dat files

    Outputs a normal 128x128 image and a large image, 1024x1024
    """
    src_path = args.src_path
    dest_path = args.output_dir.rstrip('/')
    files = os.listdir(src_path)
    pattern = "map*.dat"

    _logger.info("Generating maps from {0}".format(dest_path))

    for entry in files:
        if fnmatch.fnmatch(entry, pattern):
            print("Generating image for {0}".format(entry))
            maps.generate_image(
                "{0}/{1}".format(src_path, entry),
                dest_path,
                entry,
                False
            )

    _logger.info("Done generating images for maps")


def chunk_relocate(args):
    """Relocate chunks from (point 1, point 2) to new map at dest point
    Args:
      args ([str]): command line parameter list
    """
    _logger.info("Starting the chunk relocation")
    range1 = args.point1.split(',')
    range2 = args.point2.split(',')

    offset_coord = list(map(int, args.dest_point.split(',')))
    ranges = list(map(int, range1 + range2))

    calculate_regions(ranges, offset_coord, args.src_path, args.dest_path)


def parse_region_file(args):
    src_path = args.src_path
    nbt_data = []

    debug = True if args.loglevel == 'DEBUG' else False
    nbt_data = region.load_region(src_path, debug)

    region.save_region(src_path, nbt_data)

    if debug:
        nbt.pretty_print_nbt_data(nbt_data['chunk'])


def parse_nbt_file(args):
    src_path = args.src_path
    nbt_data = []

    # nbt files that are not gzipped
    if args.unpacked_nbt:
        nbt_data = nbt.read_nbt_file(src_path)
    # gzipped nbt, need to unpack before reading
    else:
        nbt_data = nbt.unpack_nbt_file(src_path)

    if args.loglevel == 'DEBUG':
        import pprint
        pprint.pprint(nbt_data)
        return
    if args.loglevel == 'INFO':
        nbt.pretty_print_nbt_data(nbt_data, 1)
        return

    return nbt_data

def nbt_to_json_dump(args):
    nbt_data = parse_nbt_file(args)
    print(json.dumps(nbt_data, indent=4))


def json_dump_to_nbt(args):
    lines = []
    with open(args.src_path, 'r') as inf:
        for line in inf:
            lines.append(line)

    dirty_data = json.loads(''.join(lines))

    dest_path = args.src_path.replace('.json', '.dat')
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    nbt_data = nbt.write_tag(buf, dirty_data)

    s_out = gzip.compress(nbt_data)
    with open(dest_path, 'wb+') as f:
        f.write(s_out)


def gen_nbt_file(args):
    src_path = args.src_path
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    lines = []

    with open(src_path, 'r') as inf:
        for line in inf:
            lines.append(line)

    dirty_data = eval(''.join(lines))
    nbt_data = nbt.write_tag(buf, dirty_data)

    s_out = gzip.compress(nbt_data)
    dest_path = 'heckle'

    with open(dest_path, 'wb+') as f:
        f.write(s_out)


def run():
    """Main run command
    """
    args = parse_args(sys.argv[1:])
    setup_logging(args.loglevel)

    if args.map_gen:
        map_generator(args)
    if args.chunk_relocator:
        chunk_relocate(args)
    if args.nbt:
        parse_nbt_file(args)
    if args.region:
        parse_region_file(args)
    if args.gen_nbt:
        gen_nbt_file(args)
    if args.json_dump:
        nbt_to_json_dump(args)
    if args.json_load:
        json_dump_to_nbt(args)

if __name__ == "__main__":
    run()
