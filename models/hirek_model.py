from pydantic import BaseModel, conint, NonNegativeInt

from memory.structures.hirek import Hirek
from models.army_model import ArmyModel, UnitModel, UnitType


class HirekModel(BaseModel):
    name: str
    xp: NonNegativeInt
    attack: NonNegativeInt
    defense: NonNegativeInt
    power: NonNegativeInt
    knowledge: NonNegativeInt
    owner: NonNegativeInt
    army: ArmyModel

    @staticmethod
    def from_structure(hirek: Hirek):
        army = []
        for i in range(7):
            unit_type = hirek.unit_types[i]
            unit_count = hirek.unit_counts[i]
            army.append(UnitModel(type=UnitType(unit_type), count=unit_count))

        return HirekModel(
            name=hirek.name.decode('ascii'),
            xp=hirek.xp,
            attack=hirek.attack,
            defense=hirek.defense,
            power=hirek.power,
            knowledge=hirek.knowledge,
            owner=hirek.owner,
            army=ArmyModel(__root__=army)
        )
