from enum import Enum
from typing import NamedTuple

from jungle_chess.constants import *


class PieceProperties(NamedTuple):
    """Piece type properties."""

    rank: int
    init_pos: Position


class PieceType(PieceProperties, Enum):
    """Piece types."""

    RAT = PieceProperties(rank=1, init_pos=(6, 2))
    CAT = PieceProperties(rank=2, init_pos=(1, 1))
    DOG = PieceProperties(rank=3, init_pos=(5, 1))
    WOLF = PieceProperties(rank=4, init_pos=(2, 2))
    LEOPARD = PieceProperties(rank=5, init_pos=(4, 2))
    TIGER = PieceProperties(rank=6, init_pos=(0, 0))
    LION = PieceProperties(rank=7, init_pos=(6, 0))
    ELEPHANT = PieceProperties(rank=8, init_pos=(0, 2))


class Piece:
    """A piece with it's type, color and position."""

    def __init__(self, type: PieceType, side: Side):
        col, row = type.init_pos
        if side == Side.GREEN:
            col = COLS - 1 - col
            row = ROWS - 1 - row
        self._type = type
        self._side = side
        self._pos = (col, row)

    @property
    def type(self) -> PieceType:
        """Get the type of the piece."""
        return self._type

    @property
    def side(self) -> Side:
        """Get the side of the piece."""
        return self._side

    @property
    def pos(self) -> Position:
        """Get the position of the piece."""
        return self._pos

    @property
    def rank(self) -> int:
        """Get the rank of the piece."""
        return self._type.rank

    @property
    def symbol(self) -> str:
        """Get the symbol of the piece."""
        return str(self._type.rank)

    @property
    def name(self) -> str:
        """Get the title of the piece."""
        return self._type.name.title()

    @property
    def can_jump(self) -> bool:
        """Return True if the piece can jump over a river, otherwise False."""
        return self._type in (PieceType.TIGER, PieceType.LION)

    @property
    def is_trapped(self) -> bool:
        """Return True if the piece is trapped, otherwise False."""
        return (self._side == Side.RED and self._pos in {(3, 7), (2, 8), (4, 8)}) or (
            self._side == Side.GREEN and self._pos in {(2, 0), (4, 0), (3, 1)}
        )

    def move(self, pos: Position) -> None:
        """Move the piece to the new position."""
        self._pos = pos

    def __str__(self) -> str:
        return f"{self._side.name.title()} {self.name} at {self.pos}{', trapped' if self.is_trapped else ''}"


if __name__ == "__main__":
    p = Piece(PieceType.LEOPARD, Side.RED)
    p.move((2, 8))
    print(p)
    p = Piece(PieceType.RAT, Side.GREEN)
    print(p)
