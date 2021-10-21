import typing
from ctypes import c_uint8, sizeof, Structure
from typing import Type


def structure_from_dict(
    fields: typing.Dict[str, typing.Tuple[int, Type]], min_size=None
) -> Type:
    _fields = []

    fields_list = list(fields.items())
    fields_list.sort(key=lambda k: k[1][0])
    current_offset = 0
    for key, (offset, t) in fields_list:
        assert current_offset <= offset

        padding_needed = offset - current_offset
        if padding_needed:
            _fields.append(("padding", c_uint8 * padding_needed))

        current_offset = offset + sizeof(t)

        _fields.append((key, t))

    if min_size and min_size > current_offset:
        _fields.append(("padding", c_uint8 * (min_size - current_offset)))

    class StructureFromDict(Structure):
        _pack_ = 1
        _fields_ = _fields

        def __str__(self):
            ret = ""
            for key in fields:
                ret += f"{key}: {getattr(self, key)}, "
            return ret

    return StructureFromDict


def cheat_engine_scan_string_to_regex(ce_string: str):
    ce_string = ce_string.replace(" ", "")
    ret = b""
    for i in range(len(ce_string) // 2):
        two_chars = ce_string[2 * i : 2 * (i + 1)]
        if "?" in two_chars:
            ret += b"."
        else:
            ret += bytes.fromhex(two_chars)
    return ret
