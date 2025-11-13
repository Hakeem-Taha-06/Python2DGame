from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAY = 1
    DEATH = 2
    EXIT = 3
GAME_STATE = GameState.MENU

class MenuState(Enum):
    MAIN = 0
    CHARACTER_SELECTION = 1
    DEATH = 2
MENU_STATE = MenuState.MAIN

CHARACTER = ''

class LevelState(Enum):
    MAP_1 = 0
LEVEL_STATE = LevelState.MAP_1