from ctypes import byref, memmove
from typing import Tuple

from pymem import Pymem
from pymem.pattern import pattern_scan_module
from pymem.process import module_from_name

from memory.structures.hirek import Hirek
from util.ctypes_util import cheat_engine_scan_string_to_regex

HOTA_FULL_PROC_NAME = "h3hota HD.exe"
POINTER_CALCULATION_STRING = "A1 ?? ?? ?? ?? 8B 48 ?? 83 F9 ?? 0F 84 ?? ?? 00 00 8B C1" \
                             " C1 E0 ?? 03 C1 8B 0D ?? ?? ?? ?? 8D 04 C0 8D 9C 41 ?? ?? ?? ?? 85"


class HotaException(Exception):
    pass


class HirekInTownException(HotaException):
    pass


class HirekNotSelectedException(HotaException):
    pass


class HotaMemoryReader:
    def __init__(self, hota: Pymem):
        self.hota = hota
        self.hota_module = module_from_name(hota.process_handle, HOTA_FULL_PROC_NAME)
        self.modules_base_dict = {module.name: module.lpBaseOfDll for module in self.hota.list_modules()}
        self.pointer_scan_regex = cheat_engine_scan_string_to_regex(POINTER_CALCULATION_STRING)

        what = cheat_engine_scan_string_to_regex(POINTER_CALCULATION_STRING)
        address = pattern_scan_module(self.hota.process_handle, self.hota_module, what)

        b = [n for n in hota.read_bytes(address + len(what) - 5, 4)]

        self.magic_hero_pointer_value = (255 - b[-1]) * 256 ** 3 + (255 - b[-2]) * 256 ** 2 + (255 - b[-3]) * 256 + (
                256 - b[-4])

    def _string_to_address(self, address):
        module_name, offset = address.split("+")
        return self.modules_base_dict[module_name] + int(offset, 16)

    def _read_pointer(self, address, offsets=()):
        for offset in offsets:
            address = self.hota.read_uint(address) + offset
        return address

    def read_selected_hero(self) -> Hirek:

        eax = self.hota.read_uint(self.hota_module.lpBaseOfDll + 0x29CCFC)
        ecx = self.hota.read_uint(eax + 4)

        return self.read_hero_by_number(ecx)

    def read_hero_by_number(self, hero_number):
        r = self.magic_hero_pointer_value
        if hero_number == 255:
            raise HirekNotSelectedException()
        else:
            eax = hero_number
            eax *= 2 ** 6
            eax += hero_number
            ecx = self.hota.read_uint(self.hota_module.lpBaseOfDll + 0x299538)
            eax = eax + eax * 8
            ebx = ecx + eax * 2 - r
            in_town = self.hota.read_uint(ebx + 0x105)

            if in_town & 0x00400000:
                raise HirekInTownException()

            s = self.hota.read_bytes(ebx, 1500)
            hirek = Hirek()
            memmove(byref(hirek), s, 1500)
            return hirek

    def read_turn_number(self) -> Tuple[int, int, int]:
        day_address = self._read_pointer(self.modules_base_dict[HOTA_FULL_PROC_NAME] + 0x299538, (0x0001F63E,))
        week_address = day_address + 2
        month_address = week_address + 2

        return self.hota.read_ushort(month_address), self.hota.read_ushort(week_address), self.hota.read_ushort(
            day_address)
