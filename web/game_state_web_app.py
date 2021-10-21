import json
from typing import Optional

from fastapi import status, HTTPException
from fastapi.openapi.models import Response
from injector import inject

from models.gamestate_model import GameStateModel
from services.game_events.base_game_event import GameEvents
from services.game_state_service import GameStateService
from fastapi.routing import APIRouter


class GameStateWebApp:
    @inject
    def __init__(self, game_state_service: GameStateService):
        self.game_state_service = game_state_service
        router = APIRouter(prefix="/gs")
        self.router = router

        @router.get("/", response_model=Optional[GameStateModel])
        def _get_game_state():
            if self.game_state_service.last_known_state:
                return self.game_state_service.last_known_state
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No known state available yet.",
            )

        @router.get("/events", response_model=GameEvents)
        def _get_events():
            return GameEvents.parse_obj(self.game_state_service.events)
