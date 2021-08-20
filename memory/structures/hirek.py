from util.ctypes_util import structure_from_dict
from ctypes import *

Hirek = structure_from_dict({"x_pos": (0x00, c_uint16),
                             "y_pos": (0x02, c_uint16),
                             "owner": (0x22, c_uint8),
                             "name": (0x23, c_char * 16),
                             "unit_counts": (173, c_uint32 * 7),
                             "unit_types": (145, c_uint32 * 7),
                             "level": (0x55, c_uint16),
                             "xp": (0x51, c_uint32),
                             "attack": (0x0476, c_uint8),
                             "defense": (0x477, c_uint8),
                             "power": (0x478, c_uint8),
                             "knowledge": (0x479, c_uint8),
                             "max_movement_point": (0x49, c_uint16),
                             "current_movement_points": (0x4D, c_uint16),
                             "can_use_spells": (0x430, c_uint8 * 69),
                             "secondary_skills_learned": (0x101, c_uint8),
                             "secondary_skills_level_table": (0xc9, c_uint8 * 27),
                             # doesn't seem to work :( "secondary_skills_order_table": (0xe5, c_uint8 * 27)
                             },
                            min_size=1500)
