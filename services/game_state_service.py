import logging
import time
from threading import Thread
from typing import Optional

from pymem import Pymem
from pymem.exception import PymemError

from memory.hota_memory_reader import HotaMemoryReader, HOTA_FULL_PROC_NAME
from models.gamestate_model import GameStateModel
from services.event_detectors.event_detector import GameEventDetector
from services.event_detectors.exp_gained_detector import ExpGainedDetector
from services.game_events.base_game_event import GameEvent

log = logging.getLogger(__name__)

EVENT_DETECTOR_CLASSES = [
    ExpGainedDetector
]


class GameStateService:
    def __init__(self):
        self._stop = False
        self.last_known_state = None  # type: Optional[GameStateModel]
        self.hota_reader = None  # type: Optional[HotaMemoryReader]
        self.thread = Thread(target=self._run)
        self.thread.start()
        self.events = []
        self.event_detectors = [clazz() for clazz in EVENT_DETECTOR_CLASSES]  # type: List[GameEventDetector]

    def stop(self):
        self._stop = True

    def _get_or_create_hota_reader(self):
        if not self.hota_reader or not self.hota_reader.is_connected_to_process():
            try:
                self.hota_reader = HotaMemoryReader()
            except (PymemError, AttributeError) as e:
                log.info(f"Tried creating hota reader but failed {e =}")

        return self.hota_reader

    def _append_new_events(self, new_state: GameStateModel):
        if not self.last_known_state:
            return

        for detector in self.event_detectors:
            event_or_events = detector.detect(self.last_known_state, new_state)
            if event_or_events:
                if isinstance(event_or_events, GameEvent):
                    self.events.append(event_or_events)
                elif isinstance(event_or_events, list):
                    self.events += [event for event in event_or_events if isinstance(event, GameEvent)]
                else:
                    log.warning(f"Got unexpected type returned from {detector=}, {type(event_or_events)=}")

    def _run(self):
        while not self._stop:
            time.sleep(0.1)
            try:
                reader = self._get_or_create_hota_reader()
                if not reader:
                    time.sleep(1)
                    continue

                state = GameStateModel.from_memory_reader(reader)
                self._append_new_events(state)
                self.last_known_state = state

            except PymemError as e:
                log.exception("Got an error when reading game_events state")
