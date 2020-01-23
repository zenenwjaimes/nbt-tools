
# -*- coding: utf-8 -*-
"""
Simple utility to relocate region files from [x1,y1 x2,y2] to x3,y3
offset from 0,0
"""

import argparse
import io
import sys
import logging
import shutil
import os.path
import os
import fnmatch
import gzip

from os import path
from nbt_tools import __version__
from nbt_tools.region import math
from nbt_tools.nbt import main as nbt
from nbt_tools.mcfiles import main as maps
from nbt_tools.region import main as region

__author__ = "zenen jaimes"
__copyright__ = "zenen jaimes"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def output_paths(coord_range, offset_coord):
    """Output the needed mv commands to relocate region files

    Args:
        range_coords: list
        offset_coords: list

    Returns:
      string list: commands needed to move region files
    """

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

    [output_region_cmd(
        region,
        'bb',
        'pickle'
    ) for region in mappings]


def output_region_cmd(region, from_path, to_path):
    from_xy = region[0]
    to_xy = region[1]

    src_region_file = 'r.{0}.{1}.mca'.format(*from_xy)
    src_full_file = '{0}/{1}'.format(from_path, src_region_file)

    dest_region_file = 'r.{0}.{1}.mca'.format(*to_xy)
    dest_full_file = '{0}/{1}'.format(to_path, dest_region_file)

    if (path.isfile(src_full_file)):
        try:
            shutil.copyfile(src_full_file, dest_full_file)
            print('Copied "{0}" to "{1}"\n'.format(
                src_region_file,
                dest_region_file
            ))
            ""
        except Exception:
            msg = 'Source doesn\'t exist. Failed to copy "{0}" to "{1}"\n'

            print(msg.format(
                src_region_file,
                dest_region_file
            ))

    else:
        print('Region File Exists "{0}" to "{1}"\n'.format(
            src_full_file,
            dest_full_file
        ))
        shutil.copyfile(src_full_file, dest_full_file)


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
    parser.add_argument(
        '--unpacked-nbt',
        action='store_true',
        help=help_msg,
        default=False
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--nbt', action='store_true')
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
    chunk_relocator_group.add_argument('--point1', help='(x,z) of one corner')
    chunk_relocator_group.add_argument(
        '--point2',
        help='(x,z) of opposite corner'
    )
    chunk_relocator_group.add_argument(
        '--dest-point',
        help='(x,z) destination of chunks'
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
    if args.loglevel == 'INFO':
        nbt.pretty_print_nbt_data(nbt_data, 1)


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


if __name__ == "__main__":
    run()
