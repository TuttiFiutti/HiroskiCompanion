from pydantic import BaseModel, NonNegativeInt


class PlayerModel(BaseModel):
    number: NonNegativeInt
    wood: NonNegativeInt
    stone: NonNegativeInt
    crystal: NonNegativeInt
    gem: NonNegativeInt
    mercury: NonNegativeInt
    sulfur: NonNegativeInt
    gold: NonNegativeInt
