import math

def coord_to_region(x, z):
    assert x > -30000000 and x < 30000000, "Invalid x coord"
    assert z > -30000000 and z < 30000000, "Invalid z coord"

    # add -1 to account for negative numbers
    return (math.floor(int(x / 512)),
            math.floor(int(z / 512)))

def region_to_coord(x, z):
    assert x > -58593 and x < 58593, "Invalid x coord"
    assert z > -58593 and z < 58593, "Invalid z coord"

    return (
        int(x * 512),
        int(z * 512)
    )

def region_offset(off_x, off_z):
    return lambda x, z: coord_to_region(x + off_x, z + off_z)


def coord_offset(off_x, off_z):
    return lambda x, z: (x + off_x, z + off_z)


def regions_for_range(min_x, min_z, max_x, max_z):
    assert min_x <= max_x, "min x is bigger than max x"
    assert min_z <= max_z, "min z is bigger than max z"

    # we add +1 because range uses "stop" as the stop and doesn't include
    # it, so we need to add 1 to it. we need 0 as well 
    return tuple(
            [region_x, region_z] for region_x in range(min_x, max_x + 1)
                                for region_z in range(min_z, max_z + 1)
    )

def region_mappings(regions, offset):
    return map(lambda region: tuple([tuple(region), coord_to_region(*offset(*region_to_coord(*region)))]),
            regions
    )

def get_chunk_location(x, z):
    return 4 * ((x & 31) + (z & 31) * 32)
