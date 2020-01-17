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
    output = '01 00 11 75 6E 6C 69 6D 69 74 65 64 54 72 61 63 6B 69 6E 67 00'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "byte data is not equal"


def test_tag_data_to_int():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'zCenter', 'value': -3200, 'type': 3}

    nbt_data = nbt.write_tag(buf, data)
    output = '03 00 07 7A 43 65 6E 74 65 72 FF FF F3 80'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "int data is not equal"


def test_tag_data_to_double():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'BorderCenterZ', 'value': 0, 'type': 6}

    nbt_data = nbt.write_tag(buf, data)
    output = '06 00 0D 42 6F 72 64 65 72 43 65 6E 74 65 72 5A 00 00 00 00 00 00 00 00'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "double data is not equal"


def test_tag_data_to_float():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'walkSpeed', 'value': 0.10000000149011612, 'type': 5}

    nbt_data = nbt.write_tag(buf, data)
    output = '05 00 09 77 61 6C 6B 53 70 65 65 64 3D CC CC CD'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "float data is not equal"


def test_tag_data_to_short():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'Fire', 'value': -20, 'type': 2}

    nbt_data = nbt.write_tag(buf, data)
    output = '02 00 04 46 69 72 65 FF EC'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "short data is not equal"


def test_tag_data_to_long():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'UUIDLeast', 'value': -8713279898927853564, 'type': 4}

    nbt_data = nbt.write_tag(buf, data)
    output = '04 00 09 55 55 49 44 4C 65 61 73 74 87 14 36 18 CB DA 90 04'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "short data is not equal"


def test_tag_data_to_byte_array():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)

    colors = [0x01, 0x55]
    data = {'tag_name': 'colors', 'value': colors, 'type': 7}

    nbt_data = nbt.write_tag(buf, data)
    output = '07 00 06 63 6F 6C 6F 72 73 00 00 00 02 01 55'
    expected_output = bytes.fromhex(output)

    print('expected {} got {}'.format(expected_output, nbt_data))

    assert nbt_data == expected_output, "byte array data is not equal"


def test_tag_data_to_long_array():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)

    block_states = [1229782938247303441, 1229782938247303441, 1229782938532516113]
    data = {'tag_name': 'BlockStates', 'value': block_states, 'type': 12}

    nbt_data = nbt.write_tag(buf, data)
    output = '0C 00 0B 42 6C 6F 63 6B 53 74 61 74 65 73 00 00 00 03 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 22 11 11 11'
    expected_output = bytes.fromhex(output)

    print('expected {} got {}'.format(expected_output, nbt_data))

    assert nbt_data == expected_output, "long array data is not equal"


def test_tag_data_to_int_array():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)

    # 45: Lukewarm Ocean
    # 5: Taiga
    # 19: Taiga Hills
    biomes = [45, 45, 5, 19]
    data = {'tag_name': 'Biomes', 'value': biomes, 'type': 11}

    nbt_data = nbt.write_tag(buf, data)
    output = '0B 00 06 42 69 6F 6D 65 73 00 00 00 04 00 00 00 2D 00 00 00 2D 00 00 00 05 00 00 00 13'
    expected_output = bytes.fromhex(output)

    print('expected {} got {}'.format(expected_output, nbt_data))

    assert nbt_data == expected_output, "int array data is not equal"


def test_tag_data_to_string():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    data = {'tag_name': 'WanderingTraderId', 'value': '26f2a721-4d4e-4595-a1ee-0b259d814d20', 'type': 8}

    nbt_data = nbt.write_tag(buf, data)
    output = '08 00 11 57 61 6E 64 65 72 69 6E 67 54 72 61 64 65 72 49 64 00 24 32 36 66 32 61 37 32 31 2D 34 64 34 65 2D 34 35 39 35 2D 61 31 65 65 2D 30 62 32 35 39 64 38 31 34 64 32 30'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "string data is not equal"


def test_scalar_type_tag_data_to_list():
    bio = io.BytesIO()
    buf = io.BufferedWriter(bio)
    rots = [-128.2454833984375, 16.366594314575195]
    # list of type float with 2 items
    list_data = {'value': rots, 'type': 5}
    data = {'tag_name': 'Rotation', 'value': list_data, 'type': 9}

    nbt_data = nbt.write_tag(buf, data)
    output = '09 00 08 52 6F 74 61 74 69 6F 6E 05 00 00 00 02 C3 00 3E D8 41 82 EE C9'
    expected_output = bytes.fromhex(output)

    assert nbt_data == expected_output, "list data is not equal"
