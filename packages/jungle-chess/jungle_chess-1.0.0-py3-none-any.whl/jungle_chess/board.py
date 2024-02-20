from typing import Optional, Set, FrozenSet

from jungle_chess.constants import *
from jungle_chess.piece import PieceType, Piece


class Board:
    """Gameboard."""

    def __init__(self) -> None:
        self._squares = [[None] * COLS for _ in range(ROWS)]
        self._pieces = {Side.RED: set(), Side.GREEN: set()}
        self._outcome = None
        self._init_setup()

    def _init_setup(self) -> None:
        """Initial setup."""
        for side in Side:
            for type in PieceType:
                piece = Piece(type, side)
                col, row = piece.pos
                self._squares[row][col] = piece
                self._pieces[side].add(piece)

    @property
    def outcome(self) -> Optional[Side]:
        """Return the outcome."""
        return self._outcome

    def pieces(self, side: Side) -> FrozenSet[Piece]:
        """Return the pieces of the side."""
        return frozenset(self._pieces[side])

    def get_pieces(self, side: Side) -> Set[Piece]:
        """Get all pieces of the player."""
        return self._players[side].pieces

    @staticmethod
    def is_home_den(pos: Position, side: Side) -> bool:
        """Return True if the square is the home den, otherwise False."""
        return (side == Side.RED and pos == (3, 0)) or (
            side == Side.GREEN and pos == (3, 8)
        )

    @staticmethod
    def is_opp_den(pos: Position, side: Side) -> bool:
        """Return True if the square is the opponent's den, otherwise False."""
        return (side == Side.RED and pos == (3, 8)) or (
            side == Side.GREEN and pos == (3, 0)
        )

    @staticmethod
    def is_river(pos: Position) -> bool:
        """Return True if the square is a river, otherwise False."""
        col, row = pos
        return row in {3, 4, 5} and col in {1, 2, 4, 5}

    def at(self, pos: Position) -> Optional[Piece]:
        """A piece at the position, None if the square is empty."""
        col, row = pos
        return self._squares[row][col]

    def legal_moves(self, pos: Position) -> set:
        """Return a set of legal moves for the piece."""
        src_col, src_row = pos
        src_obj = self.at(pos)
        moves = set()

        if src_obj is not None:
            for step in {(-1, 0), (0, 1), (1, 0), (0, -1)}:
                col, row = src_col + step[0], src_row + step[1]

                if (0 <= col < COLS) and (0 <= row < ROWS):
                    # Exclude the home den.
                    if Board.is_home_den((col, row), src_obj.side):
                        continue

                    # Exclude river squares if the piece is not the Rat or can't jump.
                    if (
                        Board.is_river((col, row))
                        and src_obj.type != PieceType.RAT
                        and not src_obj.can_jump
                    ):
                        continue

                    # Exclude different surface attack of the Rat.
                    if (
                        src_obj.type == PieceType.RAT
                        and Board.is_river((col, row)) != Board.is_river(pos)
                        and self.at((col, row)) is not None
                    ):
                        continue

                    # For jumping pieces apply jump across a river
                    # and exclude jumping over rats.
                    if src_obj.can_jump:
                        while Board.is_river((col, row)):
                            if self.at((col, row)) is not None:
                                continue
                            col += step[0]
                            row += step[1]

                    dst_obj = self.at((col, row))

                    # Exclude invalid captures.
                    if dst_obj is not None:
                        if dst_obj.side == src_obj.side:
                            continue

                        if not dst_obj.is_trapped:

                            # The Elephant can't capture the Rat.
                            if (
                                dst_obj.type == PieceType.RAT
                                and src_obj.type == PieceType.ELEPHANT
                            ):
                                continue

                            # A lower rank piece can't capture a higher rank one.
                            # Only The Rat can capture the Elephant.
                            if dst_obj.rank > src_obj.rank and not (
                                dst_obj.type == PieceType.ELEPHANT
                                and src_obj.type == PieceType.RAT
                            ):
                                continue

                    moves.add((col, row))

        return moves

    def move(self, src_pos: Position, dst_pos: Position) -> None:
        """Make the legal move."""
        if dst_pos not in self.legal_moves(src_pos):
            return

        src_col, src_row = src_pos
        dst_col, dst_row = dst_pos
        src_obj = self.at(src_pos)
        dst_obj = self.at(dst_pos)

        side = src_obj.side
        opp_side = Side.opposite(side)

        self._squares[src_row][src_col] = None
        self._squares[dst_row][dst_col] = src_obj
        src_obj.move(dst_pos)

        if dst_obj is not None:
            self._pieces[opp_side].remove(dst_obj)

        if Board.is_opp_den(dst_pos, side) or len(self._pieces[opp_side]) == 0:
            self._outcome = side

    def __str__(self):
        board = "   ┌─────────────┐\n"
        for row in range(ROWS - 1, -1, -1):
            board += f"{row + 1:>2} │" + (
                " ".join(
                    (
                        piece.symbol
                        if piece
                        else ("▒" if Board.is_river((col, row)) else ".")
                    )
                    for col, piece in enumerate(self._squares[row])
                )
                + "│\n"
            )
        board += "   └─────────────┘\n"
        board += "    a b c d e f g\n\n"
        return f"{board}"


if __name__ == "__main__":
    b = Board()
    print(b)
