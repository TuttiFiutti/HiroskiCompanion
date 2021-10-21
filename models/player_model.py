from pydantic import BaseModel, NonNegativeInt

from memory.structures.player import Player


class PlayerModel(BaseModel):
    number: NonNegativeInt
    wood: NonNegativeInt
    stone: NonNegativeInt
    crystal: NonNegativeInt
    gem: NonNegativeInt
    mercury: NonNegativeInt
    sulfur: NonNegativeInt
    gold: NonNegativeInt
    name: str

    @staticmethod
    def from_structure(player: Player):
        return PlayerModel(
            number=player.number,
            wood=player.wood,
            stone=player.stone,
            crystal=player.crystal,
            gem=player.gem,
            mercury=player.mercury,
            sulfur=player.sulfur,
            gold=player.gold,
            name=player.name.decode("ascii"),
        )
