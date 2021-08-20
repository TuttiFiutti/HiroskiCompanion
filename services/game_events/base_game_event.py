from datetime import datetime
from enum import Enum
from typing import Any, Optional, List

from pydantic import BaseModel


class GameEventType(Enum):
    GAME_STARTED = 0
    GAME_ENDED = 1
    GAME_RESTARTED = 2
    HERO_BOUGHT = 3
    HERO_LEVELED_UP = 4
    HERO_GAINED_XP = 5


class GameEvent(BaseModel):
    when: datetime
    type: GameEventType
    payload: Optional[Any]


def game_event(type_: GameEventType, payload: Optional[Any] = None):
    return GameEvent(when=datetime.utcnow(), type=type_, payload=payload)


class GameEvents(BaseModel):
    __root__: List[GameEvent]
