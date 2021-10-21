from typing import List

from pydantic import BaseModel, PositiveInt, NonNegativeInt

from memory.hota_memory_reader import HotaMemoryReader
from models.hirek_model import HirekModel
from models.player_model import PlayerModel

NUMBER_OF_HEROES = 179


class GameStateModel(BaseModel):
    day: NonNegativeInt
    week: NonNegativeInt
    month: NonNegativeInt

    players: List[PlayerModel]

    heroes: List[HirekModel]

    @staticmethod
    def from_memory_reader(reader: HotaMemoryReader):
        month, week, day = reader.read_turn_number()

        players = [
            PlayerModel.from_structure(reader.read_player_structure_by_number(i))
            for i in range(8)
        ]

        heroes = [
            HirekModel.from_structure(reader.read_hero_by_number(i))
            for i in range(NUMBER_OF_HEROES)
        ]

        return GameStateModel(
            day=day, week=week, month=month, players=players, heroes=heroes
        )
