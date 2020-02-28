_BOARD_WIDTH = 8
_BOARD_HEIGHT = 8


def generate_rook_moveset(curr_position, board, owner="white"):
    """
    :param curr_position: tuple containing the piece's current
                          grid coordinates (y, x)
    :return moveset: list of tuples containing possible final
                     coordinates of piece after move
    """
    curr_y = curr_position[0]
    curr_x = curr_position[1]

    # Vertical movements
    vertical_moves = [(y, curr_x) for y in range(curr_y+1, _BOARD_HEIGHT)] + \
                        [(y, curr_x) for y in range(0, curr_y)]

    # Horizontal movements
    horizontal_moves = [(curr_y, x) for x in range(curr_x+1, _BOARD_WIDTH)] + \
                        [(curr_y, x) for x in range(0, curr_x)]

    # Filter for collisions with other pieces
    for i in range(_BOARD_HEIGHT):
        for j in range(_BOARD_WIDTH):

            # Don't need to check for collisions with own piece
            if (i, j) == (curr_y, curr_x):
                continue

            # Check to see if there's a piece at the position
            # being evaluated
            piece = board[i][j]
            if not piece:
                continue

            (color, _) = piece

            # If there is a collision, remove that position from
            # moveset as well as other positions further along
            # axis. (NOTE: we can move to a position occupied by
            # an opponent's piece, but not a position further along
            # that axis)
            if (i, j) in vertical_moves:
                idx = vertical_moves.index((i, j))

                if color == owner:
                    vertical_moves = vertical_moves[:idx]
                else:
                    vertical_moves = vertical_moves[:idx+1]

            elif (i, j) in horizontal_moves:
                idx = horizontal_moves.index((i, j))

                if color == owner:
                    horizontal_moves = horizontal_moves[:idx]
                else:
                    vertical_moves = vertical_moves[:idx+1]

            else:
                continue

    moveset = vertical_moves + horizontal_moves

    return moveset

def generate_bishop_moveset(curr_position, board, owner="white"):
    """
    : param curr_position: tuple containing the piece's current grid
                           coordinates (y,x)
    : return moveset: list of tuples containing coordinates that the
                      piece can move to in the next turn
    """
    curr_y = curr_position[0]
    curr_x = curr_position[1]

    # Northeast axis
    if (_BOARD_HEIGHT - curr_y) > (_BOARD_WIDTH - curr_x):
        diagonal_NE = [(curr_y+i, curr_x+i) for i in range(1, _BOARD_WIDTH - curr_x+1)]
    else:
        diagonal_NE = [(curr_y+i, curr_x+i) for i in range(1, _BOARD_HEIGHT - curr_y+1)]

    # Northwest axis
    if (_BOARD_HEIGHT - curr_y) > curr_x:
        diagonal_NW = [(curr_y+i, curr_x-i) for i in range(1, curr_x+1)]
    else:
        diagonal_NW = [(curr_y+i, curr_x-1) for i in range(1, _BOARD_HEIGHT - curr_y+1)]

    # Southeast axis
    if curr_y > (_BOARD_WIDTH - curr_x):
        diagonal_SE = [(curr_y-i, curr_x+i) for i in range(1, _BOARD_WIDTH - curr_x+1)]
    else:
        diagonal_SE = [(curr_y-i, curr_x+i) for i in range(1, curr_y+1)]

    # Southwest aaxis
    if curr_y > curr_x:
        diagonal_SW = [(curr_y-i, curr_x-i) for i in range(1, curr_x+1)]
    else:
        diagonal_SW = [(curr_y-i, curr_x-i) for i in range(1, curr_y+1)]

    # Filter for collisions
    for i in range(len(_BOARD_HEIGHT)):
        for j in range(len(_BOARD_WIDTH)):
            # Don't need to check for collisions with own piece
            if (i, j) == (curr_y, curr_x):
                continue

            piece = board[i][j]
            (color, _) = piece

            # If there is a collision, remove that position from
            # moveset as well as other positions further along
            # axis. (NOTE: we can move to a position occupied by
            # an opponent's piece, but not a position further along
            # that axis)
            if color == owner:

                if (i, j) in diagonal_NE:
                    idx = diagonal_NE.index((i, j))

                    if color == owner:
                        diagonal_NE = diagonal_NE[:idx]
                    else:
                        diagonal_NE = diagonal_NE[:idx+1]

                elif (i, j) in diagonal_NW:
                    idx = diagonal_NW.index((i, j))

                    if color == owner:
                        diagonal_NW = diagonal_NW[:idx]
                    else:
                        diagonal_NW = diagonal_NW[:idx+1]

                elif (i, j) in diagonal_SE:
                    idx = diagonal_SE.index((i, j))

                    if color == owner:
                        diagonal_SE = diagonal_SE[:idx]
                    else:
                        diagonal_SE = diagonal_SE[:idx+1]

                elif (i, j) in diagonal_SW:
                    idx = diagonal_NE.index((i, j))

                    if color == owner:
                        diagonal_SW = diagonal_SW[:idx]
                    else:
                        diagonal_SW = diagonal_SW[:idx+1]

                else:
                    continue

    moveset = diagonal_NE + diagonal_NW + diagonal_SE + diagonal_SW

    return moveset

def generate_queen_moveset(curr_position, board, owner="white"):

    # The queen's moveset is simply a combination of the rook's and the
    # bishop's, so just generate both of those and sum them to create
    # the queen's moveset
    bishop_moveset = generate_bishop_moveset(curr_position)
    rook_moveset = generate_rook_moveset(curr_position)

    moveset = bishop_moveset + rook_moveset

    return moveset

def generate_knight_moveset(curr_position):





