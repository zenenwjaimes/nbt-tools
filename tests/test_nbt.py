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


def test_tag_data_to_bytes():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio) 
    data = {'tag_name': 'unlimitedTracking', 'value': 0, 'type': 1}

    nbt_data = nbt.write_tag(buf, data)
    raw_bytes = bytes.fromhex('01 00 11 75 6E 6C 69 6D 69 74 65 64 54 72 61 63 6B 69 6E 67 00')

    assert nbt_data == raw_bytes, "data is not equal"
