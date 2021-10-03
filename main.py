import logging
import time
from logging import INFO

from fastapi import FastAPI
from flask import Flask
from injector import Injector
from pymem.process import module_from_name
from pymem.pattern import pattern_scan_module

from memory.hota_memory_reader import HOTA_FULL_PROC_NAME, POINTER_CALCULATION_STRING, HotaMemoryReader, \
    HirekNotSelectedException
from models.army_model import UnitType
from models.gamestate_model import GameStateModel
from models.hirek_model import HirekModel
from util.ctypes_util import cheat_engine_scan_string_to_regex

from pymem import Pymem
from ctypes import *

from web.game_state_web_app import GameStateWebApp

injector = Injector()
game_state_web_app = injector.get(GameStateWebApp)
app = FastAPI()
FORMAT = '%(asctime)-15s %(message)s'
app.include_router(game_state_web_app.router)
logging.basicConfig(format=FORMAT, level=INFO)
