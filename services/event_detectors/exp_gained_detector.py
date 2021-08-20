from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, PositiveInt, NonNegativeInt

from models.gamestate_model import GameStateModel, NUMBER_OF_HEROES
from services.event_detectors.event_detector import GameEventDetector
from services.game_events.base_game_event import GameEvent, GameEventType, game_event


class ExpGainedPayload(BaseModel):
    exp_gained: PositiveInt
    which_hero: NonNegativeInt


class LevelGainedPayload(BaseModel):
    exp_gained_event: GameEvent

    levels_gained: PositiveInt
    attack_gained: NonNegativeInt
    defense_gained: NonNegativeInt
    power_gained: NonNegativeInt
    knowledge_gained: NonNegativeInt


class ExpGainedDetector(GameEventDetector):
    def detect(self, previous_state: GameStateModel, current_state: GameStateModel) -> \
            Optional[Union[GameEvent, List[GameEvent]]]:
        events = []

        number_of_heroes_that_lost_exp = 0

        for i, (hero_previously, hero_currently) in enumerate(zip(previous_state.heroes, current_state.heroes)):
            xp_diff = hero_currently.xp - hero_previously.xp

            if xp_diff > 0:
                xp_gained_payload = ExpGainedPayload(exp_gained=xp_diff, which_hero=i)
                xp_gained_event = game_event(type_=GameEventType.HERO_GAINED_XP,
                                             payload=xp_gained_payload)

                events.append(xp_gained_event)

            if xp_diff < 0:
                number_of_heroes_that_lost_exp += 1

        if number_of_heroes_that_lost_exp > 10:
            events.append(game_event(type_=GameEventType.GAME_RESTARTED))

        return events
