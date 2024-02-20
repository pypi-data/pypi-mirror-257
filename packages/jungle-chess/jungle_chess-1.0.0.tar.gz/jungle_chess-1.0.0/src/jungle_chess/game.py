import os
from typing import Final, Optional, Tuple
from string import ascii_letters, digits
from math import sqrt
from enum import Enum
from random import choice
from threading import Thread
from dataclasses import dataclass
import pickle

import pygame as pg
from pygame.locals import *
import pygame_menu as pgm

from jungle_chess.constants import *
from jungle_chess.network import Host, Server, Client
from jungle_chess.board import Board
from jungle_chess.version import __version__

# Pathes.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# Fonts.
FONT_MENU = os.path.join(FONTS_DIR, "MountainsofChristmas-Bold.ttf")
FONT_REGULAR = os.path.join(FONTS_DIR, "Roboto-Regular.ttf")
FONT_BOLD = os.path.join(FONTS_DIR, "Roboto-Bold.ttf")
FONT_TIME = os.path.join(FONTS_DIR, "aoyagireisyosimo2 Regular.ttf")

PIECE_BG = os.path.join(IMAGES_DIR, "piece_bg.png")

VALID_CHARS = list(ascii_letters + digits + ".-")

TIMEREVENT = pg.USEREVENT + 1


class GameState(Enum):
    """Game state."""

    INIT = 0
    READY = 1
    MOVE = 2
    OPP_MOVE = 3
    GAMEOVER = 4


class GameResult(Enum):
    """Game result."""

    WON = 0
    LOST = 1
    TIMEOVER = 2
    ERROR = 3


MESSAGES: Final = {
    "init": 'Click the "Ready" button',
    "ready": "Waiting for the opponent...",
    "won": "You WON! Press any key to continue",
    "lost": "You LOST. Press any key to continue",
    "timeover": "Time is over. Press any key to continue",
    "error": "Connection error. Press any key to continue",
    "surrender": "Press Y to surrender or any other key to cancel",
}

SOUNDS: Final = {
    "ready": "ready.ogg",
    "move": "slide.ogg",
    "attack": "attack.ogg",
    "won": "fanfare-finish.ogg",
    "lost": "bomb.ogg",
    "timeover": "finish.ogg",
    "error": "finish.ogg",
}


@dataclass
class Arrow:
    """Arrow."""

    side: Side
    dir: Dir
    pos: Position


class GameApp:
    """Game application class."""

    _is_server: bool
    _host: Optional[Host]
    _side: Optional[Side]
    _turn: Side
    _ready_cnt: int
    _board: Board
    _selected: Optional[Position]
    _legal_moves: set
    _selected_surf: Optional[pg.Surface]
    _legal_moves_surf: Optional[pg.Surface]
    _arrow: Optional[Arrow]
    _pieces: dict
    _message: Optional[str]
    _is_surrender: bool
    _timer_on: bool
    _timer_main_me: int
    _timer_main_opp: int
    _countdown: int
    _timer_rect: Optional[pg.Rect]

    def __init__(self) -> None:
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._table_img = pg.image.load(os.path.join(IMAGES_DIR, "table.png"))
        pg.display.set_caption(f"Jungle Chess (Dou Shou Qi)")
        pg.display.set_icon(pg.image.load(os.path.join(IMAGES_DIR, "icon.png")))
        self._clock = pg.time.Clock()

        pg.time.set_timer(TIMEREVENT, 1000)

        # Music.
        pg.mixer.music.load(os.path.join(SOUNDS_DIR, "Chinese New Year Is Coming.ogg"))
        pg.mixer.music.set_volume(0.1)

        # Sounds.
        self._sounds = {
            action: pg.mixer.Sound(os.path.join(SOUNDS_DIR, file))
            for action, file in SOUNDS.items()
        }

        # Gameboard.
        self._gameboard_surf = pg.Surface(BOARD_SIZE, pg.SRCALPHA, 32).convert_alpha()

        # Buttons.
        surf = pg.Surface(BTN_SIZE, pg.SRCALPHA, 32).convert_alpha()
        self._button_rect = surf.get_rect(topleft=(BTN_LEFT, BTN_TOP))

        ## Ready.
        self._button_ready_surf = surf.copy()
        pg.draw.rect(
            self._button_ready_surf,
            Color.BTN_BG.value,
            surf.get_rect(),
            border_radius=5,
        )
        pg.draw.rect(
            self._button_ready_surf,
            Color.BTN_FG.value,
            surf.get_rect(),
            1,
            border_radius=5,
        )
        font = pg.font.Font(FONT_REGULAR, 14)
        text = font.render("Ready", True, Color.BTN_FG.value)
        self._button_ready_surf.blit(
            text, text.get_rect(center=(BTN_WIDTH // 2, BTN_HEIGHT // 2))
        )

        ## Surrender.
        self._button_surrender_surf = surf.copy()
        pg.draw.rect(
            self._button_surrender_surf,
            Color.BTN_BG.value,
            surf.get_rect(),
            border_radius=5,
        )
        pg.draw.rect(
            self._button_surrender_surf,
            Color.BTN_FG.value,
            surf.get_rect(),
            1,
            border_radius=5,
        )
        img = pg.image.load(os.path.join(IMAGES_DIR, "flag.svg")).convert_alpha()
        pg.PixelArray(img).replace((0, 0, 0), Color.BTN_FG.value)
        img = pg.transform.smoothscale(
            img, (BTN_HEIGHT * BTN_IMG_SCALE, BTN_HEIGHT * BTN_IMG_SCALE)
        )
        self._button_surrender_surf.blit(
            img,
            img.get_rect(center=(BTN_WIDTH // 2, BTN_HEIGHT // 2)),
        )

        # Arrows.
        self._arrow_images = {}
        img = pg.image.load(os.path.join(IMAGES_DIR, "arrow.svg")).convert_alpha()
        pg.PixelArray(img).replace((255, 255, 255), Color.SQ_MARK.value)
        self._arrow_images[Side.RED] = img.copy()
        pg.PixelArray(self._arrow_images[Side.RED]).replace((0, 0, 0), Color.RED.value)
        self._arrow_images[Side.RED] = pg.transform.smoothscale(
            self._arrow_images[Side.RED], SQ_SIZE
        )
        self._arrow_images[Side.GREEN] = img.copy()
        pg.PixelArray(self._arrow_images[Side.GREEN]).replace(
            (0, 0, 0), Color.GREEN.value
        )
        self._arrow_images[Side.GREEN] = pg.transform.smoothscale(
            self._arrow_images[Side.GREEN], SQ_SIZE
        )

        # Group of pieces' sprites.
        self._pieces_gr = pg.sprite.Group()

        # Reset.
        self._reset()

        # Avatar.
        if self._side == Side.RED:
            ava = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_red.svg")
            ).convert_alpha()
            ava_d = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_red_d.svg")
            ).convert_alpha()
            ava_opp = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_green.svg")
            ).convert_alpha()
            ava_opp_d = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_green_d.svg")
            ).convert_alpha()
        else:
            ava = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_green.svg")
            ).convert_alpha()
            ava_d = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_green_d.svg")
            ).convert_alpha()
            ava_opp = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_red.svg")
            ).convert_alpha()
            ava_opp_d = pg.image.load(
                os.path.join(IMAGES_DIR, "avatar_red_d.svg")
            ).convert_alpha()

        ava = pg.transform.flip(ava, True, False)
        ava_d = pg.transform.flip(ava_d, True, False)

        ava = pg.transform.smoothscale(ava, AVA_SIZE)
        ava_d = pg.transform.smoothscale(ava_d, AVA_SIZE)
        ava_opp = pg.transform.smoothscale(ava_opp, AVA_SIZE)
        ava_opp_d = pg.transform.smoothscale(ava_opp_d, AVA_SIZE)

        # My move.
        self._my_move_surf = pg.Surface(INFO_SIZE, pg.SRCALPHA, 32).convert_alpha()
        self._my_move_surf.blit(ava, (0, 0))
        self._my_move_surf.blit(ava_opp_d, ava_opp_d.get_rect(topright=(INFO_WIDTH, 0)))

        # Opp's move.
        self._opp_move_surf = pg.Surface(INFO_SIZE, pg.SRCALPHA, 32).convert_alpha()
        self._opp_move_surf.blit(ava_d, (0, 0))
        self._opp_move_surf.blit(ava_opp, ava_opp.get_rect(topright=(INFO_WIDTH, 0)))

    def _reset(self) -> None:
        """Reset the game."""
        self._is_server = True
        self._host = None
        self._side = None
        self._turn = Side.RED
        self._ready_cnt = 0
        self._board = Board()
        self._selected = None
        self._legal_moves = set()
        self._selected_surf = None
        self._legal_moves_surf = None
        self._arrow = None
        self._pieces = {}
        self._message = None
        self._is_surrender = False
        self._timer_on = False
        self._timer_main_me = TIME_MAIN
        self._timer_main_opp = TIME_MAIN
        self._countdown = 0
        self._timer_rect = None
        self._show_menu()

    @staticmethod
    def is_river(pos: Position) -> bool:
        """Return True if the position is a river, otherwise False."""
        col, row = pos
        return row in {3, 4, 5} and col in {1, 2, 4, 5}

    def _show_menu(self) -> None:
        """Show menu."""
        bg_img = pgm.baseimage.BaseImage(os.path.join(IMAGES_DIR, "menu_bg.jpg"))
        font = pg.font.Font(FONT_MENU, 32)
        theme = pgm.Theme(
            background_color=bg_img,
            widget_font_color=Color.MENU_ITEM.value,
            selection_color=Color.MENU_SELECTED.value,
            widget_selection_effect=pgm.widgets.SimpleSelection(),
            widget_font=font,
            title=False,
        )

        ## Connection menu.
        conn_menu = pgm.Menu(
            "Connection", width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=theme
        )
        conn_menu.add.label("Waiting for opponent...")
        conn_menu.add.button("Cancel", pgm.events.RESET)

        ## Address menu.
        addr_menu = pgm.Menu(
            "Server Address", width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=theme
        )
        self._srv_addr = addr_menu.add.text_input(
            "Server address: ",
            default="127.0.0.1",
            maxchar=25,
            valid_chars=VALID_CHARS,
            onreturn=None,
        )
        addr_menu.add.button("Connect", conn_menu)
        addr_menu.add.button("Cancel", pgm.events.BACK)

        ## Main menu.
        main_menu = pgm.Menu(
            "Main Menu", width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=theme
        )

        main_menu.add.button("Start new game", conn_menu)
        main_menu.add.button("Connect to game server...", addr_menu)
        main_menu.add.button("Quit", pgm.events.EXIT)
        lbl_version = main_menu.add.label(
            f"v{__version__}",
            font_name=FONT_REGULAR,
            font_color=Color.MENU_LOGO.value,
            font_size=16,
            float=True,
            float_origin_position=True,
        )
        lbl_version.translate(620, 650)

        if not pg.mixer.music.get_busy():
            pg.mixer.music.play(-1)

        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            menu_curr = main_menu.get_current()

            if menu_curr == main_menu:
                self._is_server = True
                if self._host is not None:
                    Thread(target=self._host.disconnect).start()
                    self._host = None

            elif menu_curr == addr_menu:
                self._is_server = False

            elif menu_curr == conn_menu:
                if self._host is None:
                    if self._is_server:
                        self._host = Server()
                    else:
                        self._host = Client(self._srv_addr.get_value())
                    Thread(target=self._host.connect).start()
                if self._host.is_connected:
                    self._choose_side()
                    self._generate_pos()
                    self._message = MESSAGES["init"]
                    self._state = GameState.INIT
                    self._countdown = TIME_INIT
                    self._timer_on = True
                    pg.mixer.music.stop()
                    return

            main_menu.update(events)
            main_menu.draw(self._screen)
            pg.display.update()

    def _choose_side(self) -> None:
        """Choose a side."""
        if self._is_server:
            self._side = choice(list(Side))
            self._host.send(pickle.dumps(Side.opposite(self._side)))
        else:
            while True:
                data = self._host.recv()
                if data is not None:
                    break
            self._side = pickle.loads(data)

    def _generate_pos(self) -> None:
        """Generate gameboard position from the board."""
        self._pieces.clear()
        self._pieces_gr.empty()

        for side in Side:
            for piece in self._board.pieces(side):
                square = self._conv_pos(piece.pos)
                piece_spr = PieceSprite(piece.symbol, piece.side, square)
                self._pieces[square] = piece_spr
                self._pieces_gr.add(piece_spr)

    def _conv_pos(self, pos: Position) -> Position:
        """Convert the gameboard square to the board position, and vice versa."""
        col, row = pos
        if self._side == Side.RED:
            return col, ROWS - 1 - row
        else:
            return COLS - 1 - col, row

    @staticmethod
    def coords_from_sq(square: Position) -> Coords:
        """Get coords from the square."""
        col, row = square
        return col * SQ_SIDE, row * SQ_SIDE

    def _draw_screen(self) -> None:
        """Draw the screen."""
        self._screen.blit(self._table_img, (0, 0))
        self._draw_gameboard()

        # Buttons.
        if self._state == GameState.INIT:
            self._screen.blit(self._button_ready_surf, self._button_rect)
        elif (
            self._state in (GameState.MOVE, GameState.OPP_MOVE)
            and not self._is_surrender
        ):
            self._screen.blit(self._button_surrender_surf, self._button_rect)

        self._draw_info()
        self._draw_message()

    def _draw_gameboard(self) -> None:
        """Draw the gameboard."""
        self._gameboard_surf.fill((0, 0, 0, 0))
        self._draw_selected()
        self._draw_legal_moves()
        self._draw_pieces()
        self._draw_arrow()
        self._screen.blit(self._gameboard_surf, (BOARD_LEFT, BOARD_TOP))

    def _draw_arrow(self) -> None:
        """Draw the arrow."""
        if self._arrow is not None:
            img = self._arrow_images[self._arrow.side].copy()
            img = pg.transform.rotate(img, self._arrow.dir.value * 90)
            rect = img.get_rect(topleft=GameApp.coords_from_sq(self._arrow.pos))
            self._gameboard_surf.blit(img, rect)

    def _draw_selected(self) -> None:
        """Highlight the selected square."""
        if self._selected_surf is not None:
            self._gameboard_surf.blit(
                self._selected_surf,
                self._selected_surf.get_rect(
                    topleft=GameApp.coords_from_sq(self._selected)
                ),
            )

    def _draw_legal_moves(self) -> None:
        """Draw legal moves for the selected piece."""
        if self._legal_moves_surf is not None:
            self._gameboard_surf.blit(self._legal_moves_surf, (0, 0))

    def _draw_pieces(self) -> None:
        """Draw pieces."""
        self._pieces_gr.draw(self._gameboard_surf)

    def _draw_info(self) -> None:
        """Draw the top info."""
        if self._state not in {GameState.INIT, GameState.READY}:
            info_surf = pg.Surface(INFO_SIZE, pg.SRCALPHA, 32).convert_alpha()
            rect = info_surf.get_rect(topleft=(INFO_LEFT, INFO_TOP))

            if self._turn == self._side:
                if self._countdown == 0:
                    timer = self._timer_main_me
                    color = Color.TIMER_MAIN
                else:
                    timer = self._countdown
                    color = Color.TIMER_DELAY
            else:
                if self._countdown == 0:
                    timer = self._timer_main_opp
                    color = Color.TIMER_MAIN
                else:
                    timer = self._countdown
                    color = Color.TIMER_DELAY

            mins = timer // 60
            secs = timer % 60

            font = pg.font.Font(FONT_TIME, 24)
            text = font.render(f"{mins}:{secs:02d}", True, color.value)

            if self._turn == self._side:
                info_surf.blit(self._my_move_surf, (0, 0))
                info_surf.blit(text, text.get_rect(topleft=(TIMER_LEFT_ME, TIMER_TOP)))
            else:
                info_surf.blit(self._opp_move_surf, (0, 0))
                info_surf.blit(
                    text, text.get_rect(topright=(TIMER_RIGHT_OPP, TIMER_TOP))
                )

            self._screen.blit(info_surf, rect)

    def _draw_message(self) -> None:
        """Draw popup message."""
        if self._message is not None:
            surf = pg.Surface((MSG_WIDTH, MSG_HEIGHT), pg.SRCALPHA, 32).convert_alpha()
            pg.draw.rect(surf, Color.MSG_BG.value, surf.get_rect(), border_radius=5)
            font = pg.font.Font(FONT_REGULAR, 18)
            msg = font.render(self._message, True, Color.MSG_FG.value)

            surf.blit(
                msg,
                msg.get_rect(center=(surf.get_width() // 2, surf.get_height() // 2)),
            )

            self._screen.blit(
                surf,
                surf.get_rect(
                    center=(
                        BOARD_LEFT + BOARD_WIDTH // 2,
                        BOARD_TOP + BOARD_HEIGHT // 2,
                    )
                ),
            )

    def _is_on_gameboard(self, coords: Coords) -> bool:
        """Check if the point with coords is inside the gameboard."""
        x, y = coords
        return (0 <= x - BOARD_LEFT < BOARD_WIDTH) and (
            0 <= y - BOARD_TOP < BOARD_HEIGHT
        )

    def _animate_move(self, src: Position, dst: Position) -> None:
        """Animate the move."""
        piece = self._pieces[src]
        if dst != src:
            # Calculate.
            x1, y1 = self.coords_from_sq(src)
            x2, y2 = self.coords_from_sq(dst)
            dist = int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            steps = dist // MOVE_STEP_SIZE
            step_x = (x2 - x1) // steps
            step_y = (y2 - y1) // steps

            self._sounds["move"].play()

            # Move by steps.
            for _ in range(steps):
                self._clock.tick(ANIMATION_FPS)
                piece.rect.move_ip(step_x, step_y)
                self._draw_screen()
                pg.display.update()

            # Fast positioning.
            piece.rect.update((x2, y2), SQ_SIZE)
            self._draw_screen()
            pg.display.update()

    def _move(self, src: Position, dst: Position) -> None:
        """Make the move."""
        self._timer_on = False
        src_pos = self._conv_pos(src)
        dst_pos = self._conv_pos(dst)
        src_obj = self._board.at(src_pos)
        dst_obj = self._board.at(dst_pos)

        self._board.move(src_pos, dst_pos)

        self._animate_move(src, dst)
        
        if dst_obj is not None:
            self._sounds["attack"].play()

        # Update the position.
        self._generate_pos()
        self._arrow = Arrow(side=src_obj.side, dir=self._get_dir(src, dst), pos=src)
        self._draw_screen()
        self._timer_on = True
        self._turn = Side.opposite(self._turn)

    def _get_dir(self, src: Position, dst: Position) -> Dir:
        """Get the direction ov the move."""
        col1, row1 = src
        col2, row2 = dst

        if col2 > col1:
            return Dir.RIGHT
        if col2 < col1:
            return Dir.LEFT
        if row2 > row1:
            return Dir.UP
        if row2 < row1:
            return Dir.DOWN

    def _update_selected(self) -> None:
        """Update the selected square."""
        if self._selected is not None:
            self._selected_surf = pg.Surface(SQ_SIZE, pg.SRCALPHA, 32)
            self._selected_surf.fill(Color.SQ_SELECTED.value)
        else:
            self._selected_surf = None

        # Update legal moves for the selected piece.
        if self._selected is None:
            self._legal_moves.clear()
        else:
            pos = self._conv_pos(self._selected)
            self._legal_moves = {
                self._conv_pos(move) for move in self._board.legal_moves(pos)
            }
        if self._legal_moves is not None:
            self._legal_moves_surf = pg.Surface(BOARD_SIZE, pg.SRCALPHA, 32)
            for move in self._legal_moves:
                legal_move_surf = pg.Surface(SQ_SIZE, pg.SRCALPHA, 32)
                rect = legal_move_surf.get_rect(topleft=self.coords_from_sq(move))
                legal_move_surf.fill(Color.SQ_LEGAL.value)
                self._legal_moves_surf.blit(legal_move_surf, rect)
        else:
            self._legal_moves_surf = None

    def _handle_game_result(self, result: GameResult) -> None:
        """Handle the game over result."""
        if result == GameResult.WON:
            evt = "won"
        elif result == GameResult.LOST:
            evt = "lost"
        elif result == GameResult.TIMEOVER:
            evt = "timeover"
        else:
            evt = "error"

        self._sounds[evt].play()
        self._message = MESSAGES[evt]
        self._timer_on = False
        self._state = GameState.GAMEOVER

    def run(self) -> None:
        """Main loop."""

        while True:
            self._clock.tick(FPS)

            # Events handling.
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return

                elif event.type == TIMEREVENT and self._timer_on:
                    if self._countdown > 0:
                        self._countdown -= 1
                    elif self._state in (GameState.MOVE, GameState.OPP_MOVE):
                        if self._turn == self._side:
                            if self._timer_main_me > 0:
                                self._timer_main_me -= 1
                        else:
                            if self._timer_main_opp > 0:
                                self._timer_main_opp -= 1
                    self._draw_info()

                elif event.type == pg.KEYDOWN and self._state == GameState.GAMEOVER:
                    self._reset()

                elif event.type == pg.KEYDOWN and self._is_surrender:
                    if event.key == pg.K_y:
                        self._host.send(pickle.dumps(((-1, -1), -1)))
                        self._handle_game_result(GameResult.LOST)
                        self._state = GameState.GAMEOVER
                    else:
                        self._message = None
                        self._is_surrender = False

                elif (
                    event.type == pg.MOUSEBUTTONDOWN
                    and self._timer_on
                    and not self._is_surrender
                    and self._state != GameState.GAMEOVER
                ):
                    x, y = pg.mouse.get_pos()

                    if self._state in (GameState.MOVE, GameState.OPP_MOVE):
                        if (
                            self._button_rect.collidepoint(x, y)
                            and pg.mouse.get_pressed()[0]
                        ):
                            self._message = MESSAGES["surrender"]
                            self._is_surrender = True

                    if self._state == GameState.INIT:
                        if (
                            self._button_rect.collidepoint(x, y)
                            and pg.mouse.get_pressed()[0]
                        ):
                            # Button is pressed.
                            self._ready_cnt += 1
                            self._host.send(pickle.dumps(1))
                            self._message = MESSAGES["ready"]
                            self._state = GameState.READY

                    elif self._state == GameState.MOVE:
                        if self._is_on_gameboard((x, y)):
                            # Click is inside the gameboard.
                            square = (
                                (x - BOARD_LEFT) // SQ_SIDE,
                                (y - BOARD_TOP) // SQ_SIDE,
                            )
                            pos = self._conv_pos(square)
                            piece = self._board.at(pos)

                            if self._selected is None:
                                if piece is not None and piece.side == self._side:
                                    # Select the piece.
                                    self._selected = square
                                    self._update_selected()

                            elif self._selected == square:
                                # Unselect the piece.
                                self._selected = None
                                self._update_selected()

                            elif piece is not None and piece.side == self._side:
                                # Change selection.
                                self._selected = square
                                self._update_selected()

                            elif square in self._legal_moves:
                                src, self._selected = self._selected, None
                                self._update_selected()
                                src_pos = self._conv_pos(src)
                                dst_pos = self._conv_pos(square)
                                self._host.send(
                                    pickle.dumps(
                                        ((src_pos, dst_pos), self._timer_main_me)
                                    )
                                )
                                self._move(src, square)

                                outcome = self._board.outcome
                                if outcome is not None:
                                    # Game over.
                                    if outcome == self._side:
                                        result = GameResult.WON
                                    else:
                                        result = GameResult.LOST
                                    self._handle_game_result(result)
                                else:
                                    self._countdown = TIME_DELAY
                                    self._state = GameState.OPP_MOVE

                self._draw_screen()

            # States handling.
            if self._state in (GameState.INIT, GameState.READY):
                if self._timer_on and self._countdown == 0:
                    # Setup time is over.
                    self._handle_game_result(GameResult.TIMEOVER)
                    self._draw_screen()
                elif self._ready_cnt == 2:
                    # Both players are ready.
                    self._message = None
                    self._countdown = TIME_DELAY
                    if self._side == self._turn:
                        self._state = GameState.MOVE
                    else:
                        self._state = GameState.OPP_MOVE
                    self._sounds["ready"].play()
                    self._draw_screen()
                else:
                    data = self._host.recv()
                    if data is not None:
                        try:
                            if pickle.loads(data) == 1:
                                self._ready_cnt += 1
                            else:
                                self._handle_game_result(GameResult.ERROR)
                                self._draw_screen()
                        except:
                            self._handle_game_result(GameResult.ERROR)
                            self._draw_screen()

            elif self._state == GameState.MOVE:
                if self._timer_on and self._timer_main_me == 0:
                    # Lost by timeout.
                    self._handle_game_result(GameResult.LOST)
                    self._draw_screen()

                data = self._host.recv()
                if data is not None:
                    try:
                        move = pickle.loads(data)
                        if move == ((-1, -1), -1):
                            # Opponent surrendered.
                            self._handle_game_result(GameResult.WON)
                    except:
                        self._handle_game_result(GameResult.ERROR)

            elif self._state == GameState.OPP_MOVE:
                if self._timer_on and self._timer_main_opp == 0:
                    # Won by timeout.
                    self._handle_game_result(GameResult.WON)
                    self._draw_screen()

                data = self._host.recv()
                if data is not None:
                    try:
                        move = pickle.loads(data)
                        if move == ((-1, -1), -1):
                            # Opponent surrendered.
                            self._handle_game_result(GameResult.WON)
                        else:
                            src, dst = move[0]
                            self._timer_main_opp = move[1]
                            src_pos = self._conv_pos(src)
                            dst_pos = self._conv_pos(dst)
                            self._move(src_pos, dst_pos)
                            outcome = self._board.outcome
                            if outcome is not None:
                                # Game over.
                                if outcome == self._side:
                                    result = GameResult.WON
                                else:
                                    result = GameResult.LOST
                                self._handle_game_result(result)
                            else:
                                self._countdown = TIME_DELAY
                                self._state = GameState.MOVE
                                self._draw_screen()
                    except:
                        self._handle_game_result(GameResult.ERROR)

            pg.display.update()


class PieceSprite(pg.sprite.Sprite):
    """Sprite of a piece."""

    def __init__(self, symbol: str, side: Side, square: Tuple[int, int]) -> None:
        pg.sprite.Sprite.__init__(self)
        filename = os.path.join(IMAGES_DIR, f"{symbol}_{side.name.lower()}.png")
        color = Color.RED if side == Side.RED else Color.GREEN
        self.image = pg.Surface(SQ_SIZE, pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(topleft=GameApp.coords_from_sq(square))

        # Background.
        img = pg.image.load(PIECE_BG).convert_alpha()
        rect = img.get_rect(center=(SQ_SIDE // 2, SQ_SIDE // 2))
        self.image.blit(img, rect)

        # Animal.
        img = pg.image.load(filename).convert_alpha()
        img = pg.transform.smoothscale(img, (PIECE_IMG_SIDE, PIECE_IMG_SIDE))
        rect = img.get_rect(center=(SQ_SIDE // 2, SQ_SIDE // 2))
        self.image.blit(img, rect)

        # Rank.
        font = pg.font.Font(FONT_BOLD, 12)
        text = font.render(symbol, True, color.value)
        self.image.blit(text, (SQ_SIDE // 2 - 3, 5))

    def update(self, step_x, step_y) -> None:
        """Update the coords of the piece."""
        self.rect.move_ip(step_x, step_y)
