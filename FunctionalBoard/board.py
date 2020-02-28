"""
Based off answer provided by Maarten Fabré on Stack Exchange
https://codereview.stackexchange.com/questions/231811/printing-command-line-unicode-chess-board
"""

import enum

class Color(enum.Enum):
    WHITE = 1
    BLACK = 0

class Piece(enum.Enum):
    EMPTY = enum.auto()
    PAWN = enum.auto()
    ROOK = enum.auto()
    KNIGHT = enum.auto()
    BISHOP = enum.auto()
    KING = enum.auto()
    QUEEN = enum.auto()

Characters = {
    (Color.WHITE, Piece.EMPTY): "\u25F8",
    (Color.WHITE, Piece.PAWN): "\u265F",
    (Color.WHITE, Piece.ROOK): "\u265C",
    (Color.WHITE, Piece.KNIGHT): "\u265E",
    (Color.WHITE, Piece.BISHOP): "\u265D",
    (Color.WHITE, Piece.KING): "\u265A",
    (Color.WHITE, Piece.QUEEN): "\u265B",
    (Color.BLACK, Piece.EMPTY): "\u25FC",
    (Color.BLACK, Piece.PAWN): "\u2659",
    (Color.BLACK, Piece.ROOK): "\u2656",
    (Color.BLACK, Piece.KNIGHT): "\u2658",
    (Color.BLACK, Piece.BISHOP): "\u2657",
    (Color.BLACK, Piece.KING): "\u2654",
    (Color.BLACK, Piece.QUEEN): "\u2655",
}

grid_indices_x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
grid_indices_y = ['1', '2', '3', '4', '5', '6', '7', '8']

def board_begin():
    return (
        [
            [
                (Color.WHITE, Piece.ROOK),
                (Color.WHITE, Piece.KNIGHT),
                (Color.WHITE, Piece.BISHOP),
                (Color.WHITE, Piece.QUEEN),
                (Color.WHITE, Piece.KING),
                (Color.WHITE, Piece.BISHOP),
                (Color.WHITE, Piece.KNIGHT),
                (Color.WHITE, Piece.ROOK),
            ],
            [(Color.WHITE, Piece.PAWN) for _ in range(8)],
            *[[None] * 8 for _ in range(4)],
            [(Color.BLACK, Piece.PAWN) for _ in range(8)],
            [
                (Color.BLACK, Piece.ROOK),
                (Color.BLACK, Piece.KNIGHT),
                (Color.BLACK, Piece.BISHOP),
                (Color.BLACK, Piece.QUEEN),
                (Color.BLACK, Piece.KING),
                (Color.BLACK, Piece.BISHOP),
                (Color.BLACK, Piece.KNIGHT),
                (Color.BLACK, Piece.ROOK),
            ],
        ]
    )


def flip(board):
    return [
        row[::-1] for row in reversed(board)
    ]

def display_board(board, flip_board=False, index=False):
    # Print the column indices
    if index:
        col_indices_str = ' '
        if flip_board:
            for c in reversed(grid_indices_x): col_indices_str = col_indices_str + c
        else:
            for c in grid_indices_x: col_indices_str = col_indices_str + c
        print(col_indices_str)
    for i, row in enumerate(reversed(board) if not flip_board else board):
        row_strings = [
            Characters.get(tile, Characters[(Color((i + j) % 2), Piece.EMPTY)])
            for j, tile in enumerate(row if not flip_board else row[::-1])
        ]
        if index:
            # Add in indices for rows
            if flip_board:
                row_strings.insert(0, grid_indices_y[i])
                row_strings.append(' ' + grid_indices_y[i])
            else:
                row_strings.insert(0, grid_indices_y[7-i])
                row_strings.append(' ' + grid_indices_y[7-i])
        print("".join(row_strings))
    if index:
        print(col_indices_str)

def display_captured_pieces(captured_pieces):
    """
    Prints list of captured pieces under board
    """
    white_capture_str = "White: "
    for white_piece in captured_pieces['white']:
        white_capture_str += white_piece


if __name__ == '__main__':
    board = board_begin()
    display_board(board, index=True)

    print("White Knight: \u265e")
    print("Black Queen: \u2655")
    print("White Bishop: \u265d")
    print("Black Bishop: \u2657")

