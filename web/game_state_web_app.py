import json

from models.gamestate_model import GameStateModel
from services.game_events.base_game_event import GameEvents
from services.game_state_service import GameStateService
from flask import Blueprint


class GameStateWebApp:
    def __init__(self):
        self.game_state_service = GameStateService()  # probably move to DE
        gamestate_bp = Blueprint('gs', __name__)
        self.blueprint = gamestate_bp

        @gamestate_bp.get('/')
        def _get_game_state():
            if self.game_state_service.last_known_state:
                return self.game_state_service.last_known_state.json()
            else:
                return "", 503

        @gamestate_bp.get('/schema')
        def _get_game_state_model_schema():
            return GameStateModel.schema_json()

        @gamestate_bp.get('/events')
        def _get_events():
            return GameEvents.parse_obj(self.game_state_service.events).json()

        @gamestate_bp.get('/events/schema')
        def _get_events_schema():
            return GameEvents.schema_json()
