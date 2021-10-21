from typing import Optional, Union, List

from models.gamestate_model import GameStateModel
from services.game_events.base_game_event import GameEvent


class GameEventDetector:
    def detect(
        self, previous_state: GameStateModel, current_state: GameStateModel
    ) -> Optional[Union[GameEvent, List[GameEvent]]]:
        pass
