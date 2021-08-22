from util.ctypes_util import structure_from_dict
from ctypes import *

Player = structure_from_dict({
    "wood": (0x14, c_uint32),
    "mercury": (0x18, c_uint32),
    "stone": (0x1c, c_uint32),
    "sulfur": (0x20, c_uint32),
    "crystal": (0x24, c_uint32),
    "gem": (0x28, c_uint32),
    "gold": (0x2c, c_uint32),
    "name": (0x44, c_char * 16),
    "number": (0xE0, c_uint8)
})
