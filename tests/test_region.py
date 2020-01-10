# -*- coding: utf-8 -*-
"""
Test math functions for converting x,z pairs to mc region numbers
"""
import pytest
from nbt_tools.region import math

__author__ = "zenen jaimes"
__copyright__ = "zenen jaimes"
__license__ = "mit"


def test_neg_region_to_coord():
    x = -1
    z = -1

    assert math.region_to_coord(x, z) == (-512, -512)


def test_zero_region_to_coord():
    x = 0
    z = 0

    assert math.region_to_coord(x, z) == (0, 0)


def test_1_1_region_to_coord():
    x = 1
    z = 1

    assert math.region_to_coord(x, z) == (512, 512)


def test_neg_coords_to_region_0_0():
    x = -5
    z = -513
    assert math.coord_to_region(x, z) == (-1, -2)



def test_coords_to_region_0_0():
    x = 2
    z = 59
    assert math.coord_to_region(x, z) == (0, 0)


def test_coords_to_region_1_1():
    x = 512
    z = 512
    assert math.coord_to_region(x, z) == (1, 1)


def test_coords_to_region_1_0():
    x = 512
    z = 511
    assert math.coord_to_region(x, z) == (1, 0)


def test_coords_to_region_0_1():
    x = 511
    z = 512
    assert math.coord_to_region(x, z) == (0, 1)


def test_invalid_coords():
    x = -30000000
    z = -30000000

    with pytest.raises(AssertionError):
        math.coord_to_region(x, z)


def test_coords_offset_region_1_1():
    x = 512
    z = 511
    offset_x = 0
    offset_z = 50

    offset = math.region_offset(offset_x, offset_z)
    added = offset(x, z)

    assert added == (1, 1)


def test_coords_offset_neg_region_1_1():
    x = 512
    z = 511
    offset_x = -513
    offset_z = 50

    offset = math.region_offset(offset_x, offset_z)
    added = offset(x, z)

    assert added == (-1, 1)


def test_region_offset_xz_pairs():
    x_1 = 512
    z_1 = 511
    x_2 = -65535
    z_2 = -512
    offset_x = -513
    offset_z = 5120

    offset = math.region_offset(offset_x, offset_z)
    pairs = tuple(
                map(lambda coord:
                    offset(coord[0], coord[1]),
                    [[x_1, z_1], [x_2, z_2]]
                )
    )

    assert pairs[0] == (-1, 10)
    assert pairs[1] == (-129, 9)


def test_coord_offset_xz_pairs():
    x_1 = 512
    z_1 = 511
    x_2 = -65535
    z_2 = -512
    offset_x = -513
    offset_z = 5120

    offset = math.coord_offset(offset_x, offset_z)
    pairs = tuple(
                map(lambda coord:
                    offset(coord[0], coord[1]),
                    [[x_1, z_1], [x_2, z_2]])
    )

    assert pairs[0] == (-1, 5631)
    assert pairs[1] == (-66048, 4608)


def test_region_permutations_not_empty():
    min_x = 0
    min_z = 0
    max_x = 5
    max_z = 5

    region_ranges = math.regions_for_range(min_x, min_z, max_x, max_z)

    assert len(region_ranges) != 0


def test_region_permutations_length():
    min_x = 0
    min_z = 0
    max_x = 50
    max_z = 50

    region_ranges = math.regions_for_range(min_x, min_z, max_x, max_z)

    assert len(region_ranges) == 2601


def test_section_region_mapping_offset_single_region():
    coord_range = {
            "min_x": 0,
            "min_z": 0,
            "max_x": 512,
            "max_z": 512,
    }

    offset_x = 512
    offset_z = 512
    
    offset = math.coord_offset(offset_x, offset_z) 

    min_bound = math.coord_to_region(coord_range['min_x'], coord_range['min_z'])
    max_bound = math.coord_to_region(coord_range['max_x'], coord_range['max_z'])

    regions = math.regions_for_range(min_bound[0], min_bound[1], max_bound[0], max_bound[1])
    mappings = tuple(math.region_mappings(regions, offset))

    print(mappings, sep='\n')

    assert len(mappings) == 4
    assert mappings[0] == ((0, 0), (1, 1)), "head of region mapping not valid"
    assert mappings[3] == ((1, 1), (2, 2)), "tail of region mapping not valid"


def test_b173_to_v115():
    coord_range = {
            "min_x": -1203,
            "min_z": -1342,
            "max_x": 6208,
            "max_z": 6280,
    }

    offset_x = 10000
    offset_z = -13000
    
    offset = math.coord_offset(offset_x, offset_z) 

    min_bound = math.coord_to_region(coord_range['min_x'], coord_range['min_z'])
    max_bound = math.coord_to_region(coord_range['max_x'], coord_range['max_z'])

    regions = math.regions_for_range(min_bound[0], min_bound[1], max_bound[0], max_bound[1])
    mappings = tuple(math.region_mappings(regions, offset))

    assert len(mappings) != 0


def test_region_12_20_exists_in_list():
    min_x = -10
    min_z = -10
    max_x = 30
    max_z = 30

    region_ranges = math.regions_for_range(min_x, min_z, max_x, max_z)

    assert [12, 20] in region_ranges


def test_region_12_20_doesnt_exist_in_list():
    coords = {
        "min_x": -10,
        "min_z": -10,
        "max_x": 10,
        "max_z": 10
    }

    region_ranges = math.regions_for_range(**coords)

    assert ([12, 20] in region_ranges) == False 


def test_region_for_coords_0_0_to_200_200():
    min_x = 0
    min_z = 0
    max_x = 200
    max_z = 200

    min_bound = math.coord_to_region(min_x, min_z)
    max_bound = math.coord_to_region(max_x, max_z)

    region_ranges = math.regions_for_range(
                        min_bound[0],
                        min_bound[1],
                        max_bound[0],
                        max_bound[1]
    )

    print(region_ranges)

    assert [0, 0] in region_ranges, "lower region bound does not exist" 
    assert len(region_ranges) == 1, "small bounds can't be bigger than 1 region" 


def test_region_for_coords_0_0_to_neg200_neg200():
    max_x = 0
    max_z = 0
    min_x = -200
    min_z = -200

    min_bound = math.coord_to_region(min_x, min_z)
    max_bound = math.coord_to_region(max_x, max_z)

    region_ranges = math.regions_for_range(
                        min_bound[0],
                        min_bound[1],
                        max_bound[0],
                        max_bound[1]
    )

    assert [0, 0] in region_ranges, "higher region bound does not exist" 
    assert [-1, -1] in region_ranges, "lower region bound does not exist" 
    assert len(region_ranges) == 4, "small bounds can't be bigger than 1 region" 


def test_region_for_invalid_range_x():
    min_x = 0
    min_z = 0
    max_x = -200
    max_z = 0

    min_bound = math.coord_to_region(min_x, min_z)
    max_bound = math.coord_to_region(max_x, max_z)

    with pytest.raises(AssertionError):
        region_ranges = math.regions_for_range(
                            min_bound[0],
                            min_bound[1],
                            max_bound[0],
                            max_bound[1]
        )


def test_region_for_invalid_range_z():
    min_x = 0
    min_z = 0
    max_x = 0
    max_z = -200

    min_bound = math.coord_to_region(min_x, min_z)
    max_bound = math.coord_to_region(max_x, max_z)

    with pytest.raises(AssertionError):
        region_ranges = math.regions_for_range(
                            min_bound[0],
                            min_bound[1],
                            max_bound[0],
                            max_bound[1]
        )


def test_region_min_max_bounds():
    min_x = -1210
    min_z = -1357
    max_x = 6206
    max_z = 6281

    min_bound = math.coord_to_region(min_x, min_z)
    max_bound = math.coord_to_region(max_x, max_z)

    region_ranges = math.regions_for_range(
                        min_bound[0],
                        min_bound[1],
                        max_bound[0],
                        max_bound[1]
    )

    assert [-3, -3] in region_ranges, "lower region bound does not exist" 
    assert [12, 12] in region_ranges, "max region bound does not exist" 
