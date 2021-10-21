import ctypes
import logging
from ctypes import byref, memmove
from typing import Tuple, Optional

from pymem import Pymem
from pymem.exception import PymemError
from pymem.pattern import pattern_scan_module
from pymem.process import module_from_name

from memory.structures.hirek import Hirek
from memory.structures.player import Player
from models.player_model import PlayerModel
from util.ctypes_util import cheat_engine_scan_string_to_regex
from ctypes import byref
from ctypes.wintypes import DWORD

HOTA_FULL_PROC_NAME = "h3hota.exe"
HOTA_FULL_PROC_NAME_LONG = "h3hota HD.exe"

POINTER_CALCULATION_STRING = "A1 ?? ?? ?? ?? 8B 48 ?? 83 F9 ?? 0F 84 ?? ?? 00 00 8B C1" \
                             " C1 E0 ?? 03 C1 8B 0D ?? ?? ?? ?? 8D 04 C0 8D 9C 41 ?? ?? ?? ?? 85"


log = logging.getLogger(__name__)

class HotaException(Exception):
    pass


class HirekInTownException(HotaException):
    pass


class HirekNotSelectedException(HotaException):
    pass


class HotaMemoryReader:
    def __init__(self, hota: Optional[Pymem] = None):
        self.hota = hota or self._create_pymem_for_hota()
        self.hota_module = module_from_name(self.hota.process_handle, HOTA_FULL_PROC_NAME)
        self.modules_base_dict = {module.name: module.lpBaseOfDll for module in self.hota.list_modules()}
        self.pointer_scan_regex = cheat_engine_scan_string_to_regex(POINTER_CALCULATION_STRING)

        what = cheat_engine_scan_string_to_regex(POINTER_CALCULATION_STRING)
        address = pattern_scan_module(self.hota.process_handle, self.hota_module, what)

        b = [n for n in self.hota.read_bytes(address + len(what) - 5, 4)]

        self.magic_hero_pointer_value = (255 - b[-1]) * 256 ** 3 + (255 - b[-2]) * 256 ** 2 + (255 - b[-3]) * 256 + (
                256 - b[-4])

    def _create_pymem_for_hota(self):
        try:
            return Pymem(HOTA_FULL_PROC_NAME)
        except PymemError as e:
            log.info(f"Couldn't open Pymem for {HOTA_FULL_PROC_NAME}")

        return Pymem(HOTA_FULL_PROC_NAME_LONG)


    def is_connected_to_process(self):
        if self.hota.process_handle is None:
            return False

        exit_code = DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(self.hota.process_handle, byref(exit_code))
        return exit_code.value == 259

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

    def read_hero_by_number(self, hero_number) -> Hirek:
        r = self.magic_hero_pointer_value
        if hero_number == 4294967295:
            raise HirekNotSelectedException()
        else:
            eax = hero_number
            eax *= 2 ** 6
            eax += hero_number
            ecx = self.hota.read_uint(self.hota_module.lpBaseOfDll + 0x299538)
            eax = eax + eax * 8
            ebx = ecx + eax * 2 - r
            in_town = self.hota.read_uint(ebx + 0x105)

            if in_town & 0x00400000:  # This is probably wrong?
                raise HirekInTownException()

            s = self.hota.read_bytes(ebx, 1500)
            hirek = Hirek()
            memmove(byref(hirek), s, 1500)
            return hirek

    def read_selected_player_structure(self) -> Player:
        eax = self.hota.read_uint(self.hota_module.lpBaseOfDll + 0x2977DC)
        return self.read_player_structure_by_number(eax)

    def read_player_structure_by_number(self, player_number) -> Player:
        magic_player_offset_value = 0x20AD0
        even_more_magic_offset = 136
        edx = self.hota.read_uint(self.hota_module.lpBaseOfDll + 0x299538)
        ebx = edx + magic_player_offset_value
        shift = player_number * 360
        s = self.hota.read_bytes(edx + shift + magic_player_offset_value + even_more_magic_offset, 0xE3)
        p = Player()
        memmove(byref(p), s, 0xE3)
        return p

    def read_turn_number(self) -> Tuple[int, int, int]:
        day_address = self._read_pointer(self.modules_base_dict[HOTA_FULL_PROC_NAME] + 0x299538, (0x0001F63E,))
        week_address = day_address + 2
        month_address = week_address + 2

        return self.hota.read_ushort(month_address), self.hota.read_ushort(week_address), self.hota.read_ushort(
            day_address)
