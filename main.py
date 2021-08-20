import logging
import time
from logging import INFO

from flask import Flask
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

game_state_web_app = GameStateWebApp()
app = Flask(__name__)
FORMAT = '%(asctime)-15s %(message)s'
app.register_blueprint(game_state_web_app.blueprint, url_prefix='/gs')
logging.basicConfig(format=FORMAT, level=INFO)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8090)
