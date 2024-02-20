from enum import Enum
from typing import Tuple

FPS = 15
ANIMATION_FPS = 60

# Time limits.
TIME_INIT = 300  # 5 min
TIME_MAIN = 900  # 15 min
TIME_DELAY = 5  # 5 sec

# Screen.
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Board.
ROWS = 9
COLS = 7
SQ_SIDE = 60
SQ_SIZE = (SQ_SIDE, SQ_SIDE)
BOARD_LEFT = 140
BOARD_TOP = 115
BOARD_WIDTH = SQ_SIDE * COLS
BOARD_HEIGHT = SQ_SIDE * ROWS
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
PIECE_IMG_SIDE = SQ_SIDE * 0.6

# Popup message.
MSG_WIDTH = 400
MSG_HEIGHT = 50

# Info.
INFO_TOP = 35
INFO_LEFT = 130
INFO_HEIGHT = 60
INFO_WIDTH = 440
INFO_SIZE = (INFO_WIDTH, INFO_HEIGHT)

AVA_SIZE = SQ_SIZE

# Button.
BTN_WIDTH = 60
BTN_HEIGHT = 40
BTN_LEFT = 618
BTN_TOP = 615
BTN_SIZE = (BTN_WIDTH, BTN_HEIGHT)

BTN_IMG_SCALE = 0.6

# Timer.
TIMER_TOP = 20
TIMER_LEFT_ME = 70
TIMER_RIGHT_OPP = INFO_WIDTH - 70

# Move.
MOVE_STEP_SIZE = 5

Position = Tuple[int, int]  # (col, row)
Coords = Tuple[int, int]  # (x, y)


class Color(Enum):
    """Colors."""

    # Pieces.
    RED = (195, 2, 2)
    GREEN = (0, 81, 44)

    # Squares.
    SQ_MARK = (223, 175, 76)
    SQ_SELECTED = (106, 90, 205, 80)
    SQ_LEGAL = (255, 165, 0, 80)

    # Popup message.
    MSG_BG = (255, 250, 120)
    MSG_FG = (0, 0, 0)

    # Menu.
    MENU_LOGO = (255, 255, 255)
    MENU_ITEM = (51, 51, 51)
    MENU_SELECTED = (255, 69, 69)

    # Timer.
    TIMER_MAIN = (0, 0, 0)
    TIMER_DELAY = (170, 146, 99)

    # Button.
    BTN_BG = (0, 50, 46)
    BTN_FG = (128, 128, 128)


class Dir(Enum):
    """Directions."""

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Side(Enum):
    """Side color."""

    RED = 0
    GREEN = 1

    @staticmethod
    def opposite(side):
        """Opposite side."""
        return Side.RED if side == Side.GREEN else Side.GREEN
