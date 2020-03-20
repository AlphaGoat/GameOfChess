"""
Based off answer provided by Maarten Fabré on Stack Exchange
https://codereview.stackexchange.com/questions/231811/printing-command-line-unicode-chess-board
"""

import enum
import random

# Custom Modules
from movesets import (
    GenerateRookMoveset,
    GenerateKnightMoveset,
    GenerateBishopMoveset,
    GenerateQueenMoveset,
    GeneratePawnMoveset,
    GenerateKingMoveset,
)

ascii_delimiter = 97

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
    (Color.WHITE, Piece.EMPTY):  "\u25F8",
    (Color.WHITE, Piece.PAWN):   "\u265F",
    (Color.WHITE, Piece.ROOK):   "\u265C",
    (Color.WHITE, Piece.KNIGHT): "\u265E",
    (Color.WHITE, Piece.BISHOP): "\u265D",
    (Color.WHITE, Piece.KING):   "\u265A",
    (Color.WHITE, Piece.QUEEN):  "\u265B",
    (Color.BLACK, Piece.EMPTY):  "\u25FC",
    (Color.BLACK, Piece.PAWN):   "\u2659",
    (Color.BLACK, Piece.ROOK):   "\u2656",
    (Color.BLACK, Piece.KNIGHT): "\u2658",
    (Color.BLACK, Piece.BISHOP): "\u2657",
    (Color.BLACK, Piece.KING):   "\u2654",
    (Color.BLACK, Piece.QUEEN):  "\u2655",
}

Names = {
    (Color.WHITE, Piece.EMPTY):  None,
    (Color.WHITE, Piece.PAWN):   "w_pawn",
    (Color.WHITE, Piece.ROOK):   "w_rook",
    (Color.WHITE, Piece.KNIGHT): "w_knight",
    (Color.WHITE, Piece.BISHOP): "w_bishop",
    (Color.WHITE, Piece.KING):   "w_king",
    (Color.WHITE, Piece.QUEEN):  "w_queen",
    (Color.BLACK, Piece.EMPTY):  None,
    (Color.BLACK, Piece.PAWN):   "b_pawn",
    (Color.BLACK, Piece.ROOK):   "b_rook",
    (Color.BLACK, Piece.KNIGHT): "b_knight",
    (Color.BLACK, Piece.BISHOP): "b_bishop",
    (Color.BLACK, Piece.KING):   "b_king",
    (Color.BLACK, Piece.QUEEN):  "b_queen",
}

MoveGenerators = {
    (Color.WHITE, Piece.EMPTY):  None,
    (Color.WHITE, Piece.PAWN):   GeneratePawnMoveset(owner='white'),
    (Color.WHITE, Piece.ROOK):   GenerateRookMoveset(owner='white'),
    (Color.WHITE, Piece.KNIGHT): GenerateKnightMoveset(owner='white'),
    (Color.WHITE, Piece.BISHOP): GenerateBishopMoveset(owner='white'),
    (Color.WHITE, Piece.KING):   GenerateKingMoveset(owner='white'),
    (Color.WHITE, Piece.QUEEN):  GenerateQueenMoveset(owner='white'),
    (Color.BLACK, Piece.EMPTY):  None,
    (Color.BLACK, Piece.PAWN):   GeneratePawnMoveset(owner='black'),
    (Color.BLACK, Piece.ROOK):   GenerateRookMoveset(owner='black'),
    (Color.BLACK, Piece.KNIGHT): GenerateKnightMoveset(owner='black'),
    (Color.BLACK, Piece.BISHOP): GenerateBishopMoveset(owner='black'),
    (Color.BLACK, Piece.KING):   GenerateKingMoveset(owner='black'),
    (Color.BLACK, Piece.QUEEN):  GenerateQueenMoveset(owner='black'),
}

ColorStrToEnum = {
    "white": Color.WHITE,
    "black": Color.BLACK,
}

ColorEnumToStr = {
    Color.WHITE: "white",
    Color.BLACK: "black",
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

def display_captured_pieces(captured_pieces, color):
    """
    Prints list of captured pieces under board
    """
    capture_str = ColorEnumToStr[color].upper() + ": "

    for piece in captured_pieces[color]:
        capture_str += Characters[(color, piece)]

    print(capture_str)

def player_movesets(board,
                    opponent_moveset,
                    player='white',
                    en_passant=None):

    # Generate all possible movesets
    movesets = []
    for i, row in enumerate(board):
        for j, tile in enumerate(row):

            (_, piece) = tile
            # Pawns require special params for there moveset
            # generation
            if piece == Piece.PAWN:
                moveset_generator = MoveGenerators.get(tile)
                piece_moveset = moveset_generator((i,j),
                                                  board,
                                                  en_passant)

            # Kings also require special params for there
            # moveset generation
            if piece == Piece.KING:
                # Is the king in check (i.e., is it's position in the
                # opponent's moveset? If so, it needs to move. Discard
                # all other moves in player moveset and fill with possible
                # moves for king
                if (i, j) in [end_pos for (_, end_pos) in opponent_moveset]:
                   pass

                moveset_generator = MoveGenerators.get(tile)
                piece_moveset = moveset_generator((i, j),
                                                  board,
                                                  opponent_moveset)

            else:
                moveset_generator = MoveGenerators.get(tile)
                if moveset_generator: piece_moveset = moveset_generator((i, j),
                                                                        board)

            movesets.append(piece_moveset)

def generate_movesets(board,
                      opponent_moveset,
                      player_color='white',
                      en_passant=None):
    """
    Generate all movesets available, given a certain state
    of the board
    """
    # Initialize a list to keep track of all possible moves available to player
    possible_moves = []
    for i, row in enumerate(board):
        for j, tile in enumerate(row):

            # See if the tile actually represents a piece in play.
            # If not, continue to next tile
            if not tile:
                continue

            (color, piece) = tile

            # If the piece belongs to the other player, move on
            if color != player_color:
                continue

            moveset_generator = MoveGenerators.get(tile)

            # Keep King's movesets seperate from the rest of the pieces.
            # The moveset available to the king will be dependent on the
            # movesets
            if piece == Piece.KING:

                piece_moveset = moveset_generator((i, j),
                                                  board,
                                                  opponent_moveset)

                # Is the king in check (i.e., is it's position in the
                # opponent's moveset? If so, it needs to move. Discard
                # all other moves in player moveset, fill with possible
                # moves for king, and return those moves
                if (i, j) in [end_pos for (_, end_pos) in opponent_moveset]:
                    possible_moves.clear()
                    possible_moves.extend([((i, j), move) for move in piece_moveset])
                    return possible_moves

            # The pawn's moveset varies from the rest of the pieces, as it
            # relies on the previous state of the board (did an opposing
            # pawn just move two spaces from start?)
            elif piece == Piece.PAWN:
                piece_moveset = moveset_generator((i, j),
                                                  board,
                                                  en_passant=en_passant)
            else:
                piece_moveset = moveset_generator((i, j),
                                                  board)

            possible_moves.extend([((i, j), move) for move in piece_moveset])

    return possible_moves

def human_turn(board,
               opponent_moveset,
               player_color='white',
               en_passant=None):
    """
    Generates all moves available to player based on state of
    board and presents them as options to the command line
    """
    choice_idx = ascii_delimiter
    mod = None
    moveset_dictionary = {}
    for i, row in enumerate(board):
        for j, tile in enumerate(row):

            # If the tile is not an actual piece, move on
            if not tile:
                continue

            (color, piece) = tile

            # If the piece is not the player's, move on
            if color != player_color:
                continue

            # Generate moves for player pieces
            moveset_generator = MoveGenerators.get(tile)

            if piece == Piece.KING:
                piece_moveset = moveset_generator((i, j),
                                                  board,
                                                  opponent_moveset)
            elif piece == Piece.PAWN:
                piece_moveset = moveset_generator((i, j),
                                                  board,
                                                  en_passant=en_passant)
            else:
                piece_moveset = moveset_generator((i, j),
                                                  board)

            # Convert current position of piece into grid coordinates
            pos_in_grid_coords = convert_int_to_grid_coords((i, j))
            for move in piece_moveset:
                dest_in_grid_coords = convert_int_to_grid_coords(move)

                # Present choices to players as dictionary with ordered character
                # indices as keys
                if mod:
                    print("{0}) {1} {2} -> {3}".format(chr(mod) + chr(choice_idx),
                                                       Names.get(tile),
                                                       pos_in_grid_coords,
                                                       dest_in_grid_coords))
                else:
                    print("{0}) {1} {2} -> {3}".format(chr(choice_idx),
                                                       Names.get(tile),
                                                       pos_in_grid_coords,
                                                       dest_in_grid_coords))
                if mod:
                    moveset_dictionary[chr(mod) + chr(choice_idx)] = ((i, j), move)
                else:
                    moveset_dictionary[chr(choice_idx)] = ((i, j), move)
                choice_idx += 1
                if (choice_idx - ascii_delimiter) > 25 and not mod:
                    choice_idx = ascii_delimiter
                    mod = ascii_delimiter
                elif (choice_idx - ascii_delimiter) > 25:
                    choice_idx = ascii_delimiter
                mod += 1

    return moveset_dictionary

def check_for_checkmate(board,
                        player_moveset,
                        player_color='white'):
    """
    Checks for checkmate after player has made their turn

    returns True if the king is in checkmate. Else, False
    """
    # Check if king is threatened by player pieces
    player_enum_color = ColorStrToEnum[player_color]
    for i, row in enumerate(board):
        king_coords = (i, row.index((player_enum_color, Piece.KING)))

    if king_coords in [threat_spaces for (_, threat_spaces) in player_moveset]:

        # Check if the king is able to make any moves. If not, this is checkmate
        moveset_generator = MoveGenerators((player_color, Piece.KING))
        if not moveset_generator(king_coords,
                                 board,
                                 player_moveset):
            return True

    return False

def convert_int_to_grid_coords(int_coords):
    """
    Helper function to convert integer coordinates used internally
    by pieces at play to chess grid coordinates for reference
    """
    # Convert x coord to character using ascii encoding
    x_int_coord = int_coords[0]
    y_int_coord = int_coords[1] + 1
    x_grid_coord = chr(ascii_delimiter + x_int_coord)

    # y coord stays in integer format, so that's easy
    grid_coord = x_grid_coord + str(y_int_coord)

    return grid_coord


if __name__ == '__main__':

    ########################################
    # Play a game of chess with the player #
    ########################################

    # Ask the player what color they want to play as
    while True:
        player_color = input("Choose color (white/black):")
        if player_color != 'white' and player_color != 'black':
            if player_color != 'White' and player_color != 'Black':
                print("Error: Input not understood. Try again")
            else:
                if player_color == 'White':
                    player_color = 'white'
                    break
                else:
                    player_color = 'black'
                    break
        else:
            break

    player_enum_color = ColorStrToEnum[player_color]

    # Generate board
    board = board_begin()

    # Initialize game loop
    opponent_moveset = None
    en_passant = None
    captured_pieces = {
        Color.WHITE : [],
        Color.BLACK : [],
    }

    switch = {
        Color.WHITE: Color.BLACK,
        Color.BLACK: Color.WHITE,
    }

    turn = Color.WHITE
    checkmate = False
    while not checkmate:

        # Allow player to move
        if turn == player_enum_color:
            # Generate moves available to player
            player_move_dict = player_movesets(board,
                                               opponent_moveset,
                                               player=ColorEnumToStr[turn],
                                               en_passant=en_passant)

            while True:
                for key, value in player_move_dict:
                    (row, col) = value[0]
                    piece = board[row][col]
                    print("{0}) {1}: {2} -> {3}".format(key,
                                                        piece,
                                                        value[0],
                                                        value[1]
                                                        ))

                chosen_key = input("Chose move: ")

                try:
                    move = player_move_dict[chosen_key]
                except KeyError:
                    print("Sorry, that input was not understood. Try again.")

            # Perform player chosen move
            (curr_row, curr_col), (new_row, new_col) = move
            player_piece = board[curr_row][curr_col]

            # Is there an opposing piece at that position?
            # If so, place it in captured pieces list
            if board[new_row][new_col]:
                (color, piece_type) = board[new_row][new_col]
                captured_pieces[color].append(piece_type)

            # Move piece to new position and clear old position
            board[new_row][new_col] = player_piece
            board[curr_row][curr_col] = None

        # Process computer player movement (literally just a random
        # movement generator for now)
        else:
            computer_movesets = generate_movesets(board, opponent_moveset,
                                                  player_color=turn,
                                                  en_passant=en_passant)
            r = random.randint(len(computer_movesets))
            (curr_row, curr_col), (new_row, new_col) = computer_movesets[r]

            # Perform randomly chosen move
            computer_piece = board[curr_row][curr_col]

            # Is there an opposing piece at that position?
            # If so, place it in captured pieces list
            if board[new_row][new_col]:
                (color, piece_type) = board[new_row][new_col]
                captured_pieces[color].append(piece_type)

            # move piece to new position and clear old position
            # Move piece to new position and clear old position
            board[new_row][new_col] = computer_piece
            board[curr_row][curr_col] = None

            # Generate this player's moveset after piece was moved
            # and store it for next turn, so that we can generate
            # the other player's new moveset




        # display state of board
        display_board(board)
        capt_white_pieces = captured_pieces[Color.WHITE]
        capt_black_pieces = captured_pieces[Color.BLACK]
        display_captured_pieces(capt_white_pieces, Color.WHITE)
        display_captured_pieces(capt_black_pieces, Color.BLACK)

        # Switch turns
        turn = switch[turn]











    board = board_begin()
    display_board(board, index=True)

    print("White Knight: \u265e")
    print("Black Queen: \u2655")
    print("White Bishop: \u265d")
    print("Black Bishop: \u2657")

