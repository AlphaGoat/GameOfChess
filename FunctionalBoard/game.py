import random

# Custom Modules
from board import Piece, Color, MoveGenerators, board_begin

def board_state_generator(board, en_passant=None):
    """
    Function to generate the movesets available to a player,
    given state of board

    :param board:      a BOARD_HEIGHT x BOARD_WIDTH array that contains
                       all pieces in their specific position on the board
    :param en_passant: Either None if no pawn is open to en-passant,
                       or a tuple containing the position of the pawn that
                       is open to en-passant

    :return white_moveset: movesets available to white
    :return black_moveset: movesets available to black
    """
    white_movesets = []
    black_movesets = []
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):

            # Traverse board and generate the moveset for all pieces
            # If there is not a piece at position at board, continue
            # to next position
            if not board[row][col]:
                continue

            (pcolor, piece) = board[row][col]

            moveset_generator = MoveGenerators[(pcolor, piece)]
            # Pawns require a unique input (en-passant), as the ability
            # of a pawn to perform en-passant relies on if a pawn was
            # moved last turn in a specific manner
            if piece == Piece.PAWN:
                moveset = moveset_generator((row, col), board,
                                            en_passant=en_passant)

            # Save moveset generation for king for last, as that is dependent
            # on the moveset of the other player (a king cannot place itself
            # in check)
            elif piece == Piece.KING:
                if pcolor == Color.WHITE:
                    white_king_pos = (row, col)
                else:
                    black_king_pos = (row, col)

            else:
                moveset = moveset_generator((row, col), board)

            # Add to corresponding player's moveset
            if pcolor == Color.WHITE:
                white_movesets.extend(moveset)

            else:
                black_movesets.extend(moveset)

    # Now generate kings' movesets
    wk_row, wk_col = white_king_pos
    wking = board[wk_row][wk_col]
    wk_moveset_gen = MoveGenerators[wking]
    wk_moveset = wk_moveset_gen((wk_row, wk_col),
                                board,
                                white_movesets,
                                black_movesets)
    white_movesets.extend(wk_moveset)

    bk_row, bk_col = black_king_pos
    bking = board[bk_row][bk_col]
    bk_moveset_gen = MoveGenerators[bking]
    bk_moveset = bk_moveset_gen((bk_row, bk_col),
                                board,
                                black_movesets,
                                white_movesets)

    # Cross reference black movesets and see if any of the pieces
    # place the white king in check (remember...we generated the
    # white king's moveset without knowing if any of the black king's
    # moves would place it in check
    white_movesets = filter(lambda move: (move not in wk_moveset), white_movesets)
    wk_moveset = wk_moveset_gen((wk_row, wk_col),
                                board,
                                white_movesets,
                                black_movesets)

    return white_movesets, black_movesets

def CheckForChek(board, color):

    pass

def checkForEnPassant(board, chosen_move):
    """
    Check if the piece we just moved will be open to en-passant
    next turn
    """
    (curr_row, curr_col), (new_row, new_col) = chosen_move
    (color, piece_type) = board[curr_row, curr_col]
    if piece_type == Piece.PAWN:
        # Did the pawn move two spaces from starting position?
        # If so, return coordinates of pawn open to en-passant
        if abs(curr_row - new_row) == 2:
            return (new_row, new_col)

    return None

def checkForCheckmate(white_movesets,
                      black_movesets):
   pass


def human_turn(moveset):
    """
    Generates all moves available to player based on state of
    board and presents them as options to the command line
    """
    choice_idx = ascii_delimiter
    mod = None
    moveset_dictionary = {}
    for move in moveset:
        curr_coords = move[0]
        dest_coords = move[1]
        curr_pos_in_grid = convert_int_to_grid_coords(curr_coords)
        dest_pos_in_grid = convert_int_to_grid_coords(dest_coords)

        # Present choices to players as dictionary with ordered character
        # indices as keys
        if mod:
            print("{0}) {1} {2} -> {3}".format(chr(mod) + chr(choice_idx),
                                               Names.get(tile),
                                               curr_pos_in_grid,
                                               dest_pos_in_grid))
        else:
            print("{0}) {1} {2} -> {3}".format(chr(choice_idx),
                                               Names.get(tile),
                                               curr_pos_in_grid,
                                               dest_pos_in_grid))
        if mod:
            moveset_dictionary[chr(mod) + chr(choice_idx)] = move
        else:
            moveset_dictionary[chr(choice_idx)] = move
        choice_idx += 1
        if (choice_idx - ascii_delimiter) > 25 and not mod:
            choice_idx = ascii_delimiter
            mod = ascii_delimiter
        elif (choice_idx - ascii_delimiter) > 25:
            choice_idx = ascii_delimiter
        mod += 1

    return moveset_dictionary

def choose_random_move(moveset):
    """
    The most basic of AI...as in its not an AI...
    """
    num_moves = len(moveset)
    r = random.randint(num_moves)
    return moveset[r]

if __name__ == '__main__':

    # Initialize game board
    board = board_begin()

    # init vars for game
    white_movesets = []
    black_movesets = []
    captured_pieces = {
        Color.WHITE : [],
        Color.BLACK: [],
    }
    flip_turn = {
        Color.WHITE : Color.BLACK,
        Color.BLACK : Color.WHITE,
    }
    turn = Color.WHITE
    en_passant = None

    # Run loop for game
    checkmate = False
    while not checkmate:


        if turn == Color.WHITE:
            # Is it the player's turn?
            if player == Color.WHITE:
                moveset_dict = human_turn(white_movesets)
                while(True):
                    move_key = input("Input chosen move: ")
                    try:
                        chosen_move = moveset_dict[move_key]
                        break
                    except KeyError:
                        print("Input not understood. Try again.")
                        confirmation = input("Reprint possible moves? (y/n): ")
                        if confirmation.lower() == 'y' or confirmation.lower() == 'yes':
                            moveset_dict = human_turn(white_movesets)

            else:
                chosen_move = choose_random_move(white_movesets)

        else:
            # Is it the player's turn?
            if player == Color.BLACK:
                moveset_dict = human_turn(black_movesets)
                while(True):
                    move_key = input("Input chosen move: ")
                    try:
                        chosen_move = moveset_dict[move_key]
                        break
                    except KeyError:
                        print("Input not understood. Try again.")
                        confirmation = input("Reprint possible moves? (y/n): ")
                        if confirmation.lower() == 'y' or confirmation.lower() == 'yes':
                            moveset_dict = human_turn(black_movesets)

            else:
                chosen_move = choose_random_move(black_movesets)

        # Is the piece we're moving a pawn? If so, does it open itself
        # to en-passant?
        en_passant = checkForEnPassant(board, chosen_move)

        # Enact move
        (curr_row, curr_col), (new_row, new_col) = chosen_move
        piece = board[curr_row][curr_col]

        # Is there an opponent piece where we are moving to? If so, remove it
        # and add it to list of captured pieces
        if board[new_row][new_col]:
            (color, piece_type) = board[new_row][new_col]
            captured_pieces[color].append(piece_type)

        # move piece to chosen position
        board[new_row][new_col] = piece

        # place an empty square at position piece was moved from
        board[curr_row][curr_col] = None

        # Perform check for checkmate
        checkmate = checkForCheckmate(board)

        # Generate state of the board before player makes move
        # (i.e., the movesets available to both players)
        white_movesets, black_movesets = board_state_generator(board,
                                                               en_passant=en_passant)
