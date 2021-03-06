from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel, PositiveInt, NonNegativeInt

UINT32_MAX = 4294967295


class UnitType(Enum):
    EMPTY = UINT32_MAX
    UNKNOWN = -1
    PIKEMAN = 0
    HALBERDIER = 1
    ARCHER = 2
    CROSSBOWMAN = 3
    GRIFFIN = 4
    ROYAL_GRIFFIN = 5
    SWORDSMAN = 6
    CRUSADER = 7
    MONK = 8
    ZEALOT = 9
    CAVALIER = 10
    CHAMPION = 11
    ANGEL = 12
    ARCHANGEL = 13
    CENTAUR = 14
    CENTAUR_CAPTAIN = 15
    DWARF = 16
    BATTLE_DWARF = 17
    WOOD_ELF = 18
    GRAND_ELF = 19
    PEGASUS = 20
    SILVER_PEGASUS = 21
    DENDROID_GUARD = 22
    DENDROID_SOLDIER = 23
    UNICORN = 24
    WAR_UNICORN = 25
    GREEN_DRAGON = 26
    GOLD_DRAGON = 27
    GREMLIN = 28
    MASTER_GREMLIN = 29
    STONE_GARGOYLE = 30
    OBSIDIAN_GARGOYLE = 31
    STONE_GOLEM = 32
    IRON_GOLEM = 33
    MAGE = 34
    ARCH_MAGE = 35
    GENIE = 36
    MASTER_GENIE = 37
    NAGA = 38
    NAGA_QUEEN = 39
    GIANT = 40
    TITAN = 41
    IMP = 42
    FAMILIAR = 43
    GOG = 44
    MAGOG = 45
    HELL_HOUND = 46
    CERBERUS = 47
    DEMON = 48
    HORNED_DEMON = 49
    PIT_FIEND = 50
    PIT_LORD = 51
    EFREETI = 52
    EFREET_SULTAN = 53
    DEVIL = 54
    ARCH_DEVIL = 55
    SKELETON = 56
    SKELETON_WARRIOR = 57
    WALKING_DEAD = 58
    ZOMBIE = 59
    WIGHT = 60
    WRAITH = 61
    VAMPIRE = 62
    VAMPIRE_LORD = 63
    LICH = 64
    POWER_LICH = 65
    BLACK_KNIGHT = 66
    DREAD_KNIGHT = 67
    BONE_DRAGON = 68
    GHOST_DRAGON = 69
    TROGLODYTE = 70
    INFERNAL_TROGLODYTE = 71
    HARPY = 72
    HAPRY_HAG = 73
    BEHOLDER = 74
    EVIL_EYE = 75
    MEDUSA = 76
    MEDUSA_QUEEN = 77
    MINOTAUR = 78
    MINOTAUR_KING = 79
    MANTICORE = 80
    SCORPICORE = 81
    RED_DRAGON = 82
    AFROPOLISH_DRAGON = 83
    GOBLIN = 84
    HOBOGOBLIN = 85
    WOLF_RIDER = 86
    WOLF_RAIDER = 87
    ORC = 88
    ORC_CHIEFTAIN = 89
    OGRE = 90
    OGRE_MAGE = 91
    ROC = 92
    THUNDERBIRD = 93
    CYCLOPS = 94
    CYCLOPS_KING = 95
    BEHEMOTH = 96
    ANCIENT_BEHEMOTH = 97
    GNOLL = 98
    GNOLL_MARAUDER = 99
    LIZARDMAN = 100
    LIZARD_WARRIOR = 101
    SERPENT_FLY = 102
    DRAGON_FLY = 103
    BASILISK = 104
    GREATER_BASILISK = 105
    GORGON = 106
    MIGHTY_GORGON = 107
    WYVERN = 108
    WYVERN_MONARCH = 109
    HYDRA = 110
    CHAOS_HYDRA = 111
    AIR_ELEMENTAL = 112
    EARTH_ELEMENTAL = 113
    FIRE_ELEMENTAL = 114
    WATER_ELEMENTAL = 115
    PIXIE = 118
    SPRITE = 119
    STORM_ELEMENTAL = 127
    ICE_ELEMENTAL = 123
    ENERGY_ELEMENTAL = 129
    MAGMA_ELEMENTAL = 125
    PSYCHIC_ELEMENTAL = 120
    MAGIC_ELEMENTAL = 121
    FIREBIRD = 130
    PHEONIX = 131
    GOLD_GOLEM = 116
    AZURE_DARGON = 132
    BOAR = 140
    CRYSTAL_DRAGON = 133
    DIAMOND_GOLEM = 117
    ENCHANTER = 136
    FAERIE_DRAGON = 134
    HALFLING = 138
    MUMMY = 141
    NOMAD = 142
    PEASANT = 139
    ROGUE = 143
    RUST_DRAGON = 135
    SHARPSHOOTER = 137
    TROLL = 144

    FANGARM = 168
    LEPRECHAUN = 169
    SATYR = 167
    STEEL_GOLEM = 170

    NYMPH = 153
    OCEANID = 154
    CREW_MATE = 155
    SEAMAN = 156
    PIRATE = 157
    CORSAIR = 158
    SEA_DOG = 151
    STORMBIRD = 159
    AYSSID = 160
    SEA_WITCH = 161
    SORCERESS = 162
    NIX = 163
    NIX_WARRIOR = 164
    SEA_SERPENET = 165
    HASPID = 166


class UnitModel(BaseModel):
    type: UnitType
    count: NonNegativeInt


class ArmyModel(BaseModel):
    __root__: List[UnitModel]
