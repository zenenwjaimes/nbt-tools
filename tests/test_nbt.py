# -*- coding: utf-8 -*-
"""
NBT reading
"""
import pytest
from nbt_tools.nbt import *
from nbt_tools.nbt import main as nbt
from distutils import dir_util
from pytest import fixture
import io
import os
import pprint

__author__ = "zenen jaimes"
__copyright__ = "zenen jaimes"
__license__ = "mit"

@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_nbt_zero_byte_to_int():
    byte = nbt.to_byte(b'\x00')
    
    assert byte == 0


def test_nbt_byte_to_int():
    byte = nbt.to_byte(b'\x0A')
    
    assert byte == 10


def test_nbt_byte_not_matched():
    byte = nbt.to_byte(b'\x0B')
    
    assert byte != 10


def test_nbt_data_is_list(datadir):
    nbt_path = datadir.join("nbt_test.dat")
    nbt_data = nbt.unpack_nbt_file(nbt_path)

    assert type(nbt_data) is list 


def test_nbt_int_tag(datadir):
    data = []
    raw_bytes = bytes.fromhex('03 00 07 7A 43 65 6E 74 65 72 FF FF F3 80')
    nbt_data = nbt.read_nbt_bytes(raw_bytes)

    assert nbt_data[0]['type'] == nbt.TAG.Int.value, \
            "tag isn't an INT tag"
    assert len(nbt_data[0]['tag_name']) == 0x07, "tag length isn't 07"
    assert nbt_data[0]['tag_name'] == 'zCenter', "tag name isn't zCenter"


def test_nbt_root_tag(datadir):
    data = []
    nbt_path = datadir.join("nbt_test.dat")
    nbt_data = nbt.unpack_nbt_file(nbt_path)

    assert nbt_data[0]['type'] == nbt.TAG.Compound.value, \
            "tag isn't compound tag"
    assert nbt_data[0]['tag_name'] == "root", \
            "compound tag name to start file isn't 'root'"

#def test_nbt_compound():
#
#    assert compound.read(x, z) == (-512, -512)

#def test_region_min_max_bounds():
#    min_x = -1210
#    min_z = -1357
#    max_x = 6206
#    max_z = 6281
#
#    min_bound = math.coord_to_region(min_x, min_z)
#    max_bound = math.coord_to_region(max_x, max_z)
#
#    region_ranges = math.regions_for_range(
#                        min_bound[0],
#                        min_bound[1],
#                        max_bound[0],
#                        max_bound[1]
#    )
#
#    assert [-3, -3] in region_ranges, "lower region bound does not exist" 
#    assert [12, 12] in region_ranges, "max region bound does not exist" 
