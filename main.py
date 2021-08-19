import time

from pymem.process import module_from_name
from pymem.pattern import pattern_scan_module

from memory.hota_memory_reader import HOTA_FULL_PROC_NAME, POINTER_CALCULATION_STRING, HotaMemoryReader
from models.army_model import UnitType
from util.ctypes_util import cheat_engine_scan_string_to_regex

from pymem import Pymem
from ctypes import *

hota = Pymem(HOTA_FULL_PROC_NAME)
hota_memory_reader = HotaMemoryReader(hota)

doit = True


def _int_to_enum(unit):
    try:
        return UnitType(unit)
    except Exception:
        return UnitType.UNKNOWN


while doit:
    time.sleep(1)
    try:
        now = time.time()
        for i in range(100000):
            unit_types = hota_memory_reader.read_selected_hero().name
        print(time.time()-now)
    except Exception as e:
        print(e)
    print(unit_types)
    # print([_int_to_enum(unit) for unit in unit_types])
