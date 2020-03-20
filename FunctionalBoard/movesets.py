_BOARD_WIDTH = 8
_BOARD_HEIGHT = 8



class GenerateRookMoveset(object):
    def __init__(self, color):
        self.color = color

    def __call__(self, curr_position, board):
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

                # Check if the position is in the piece's moveset.
                # If not, move on
                if (i, j) not in vertical_moves or (i, j) not in horizontal_moves:
                    continue

                # Check to see if there's a piece at the position
                # being evaluated
                piece = board[i][j]
                if not piece:
                    continue

                (color, piece_type) = piece

                # Check if the piece is the player's king. If it is, store coords
                # for later
                if (color, piece_type) = (self.color, PIECE.KING):
                    king_coords = (row, col)

                # If there is a collision, remove that position from
                # moveset as well as other positions further along
                # axis. (NOTE: we can move to a position occupied by
                # an opponent's piece, but not a position further along
                # that axis)
                if (i, j) in vertical_moves:
                    idx = vertical_moves.index((i, j))

                    if color == self.color:
                        vertical_moves = vertical_moves[:idx]
                    else:
                        vertical_moves = vertical_moves[:idx+1]

                elif (i, j) in horizontal_moves:
                    idx = horizontal_moves.index((i, j))

                    if color == self.color:
                        horizontal_moves = horizontal_moves[:idx]
                    else:
                        vertical_moves = vertical_moves[:idx+1]

                else:
                    continue

        moveset = vertical_moves + horizontal_moves

        # Filter for movesets that would place the player's King in check
        for _, (new_y, new_x) in moveset:

            # Create a new "state of the board" with the piece moved to that
            # position
            move_state = []
            for element in board:
                move_state.append(element)
            move_state[curr_y][curr_x] = None
            move_state[new_y][new_x] = (self.color, PIECE.ROOK)

            if CheckForCheck(


        return moveset

class GenerateBishopMoveset(object):
    def __init__(self, owner='white'):
        self.owner = owner

    def __call__(self, curr_position, board):
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

                # Check if the position is in the piece's moveset. If
                # not, move on to another position
                if (i,j) not in diagonal_NE or (i,j) not in diagonal_NW \
                        or (i,j) not in diagonal_SE or (i,j) not in diagonal_SW:
                    continue

                piece = board[i][j]
                (color, _) = piece

                # If there is a collision, remove that position from
                # moveset as well as other positions further along
                # axis. (NOTE: we can move to a position occupied by
                # an opponent's piece, but not a position further along
                # that axis)
                if color == self.owner:

                    if (i, j) in diagonal_NE:
                        idx = diagonal_NE.index((i, j))

                        if color == self.owner:
                            diagonal_NE = diagonal_NE[:idx]
                        else:
                            diagonal_NE = diagonal_NE[:idx+1]

                    elif (i, j) in diagonal_NW:
                        idx = diagonal_NW.index((i, j))

                        if color == self.owner:
                            diagonal_NW = diagonal_NW[:idx]
                        else:
                            diagonal_NW = diagonal_NW[:idx+1]

                    elif (i, j) in diagonal_SE:
                        idx = diagonal_SE.index((i, j))

                        if color == self.owner:
                            diagonal_SE = diagonal_SE[:idx]
                        else:
                            diagonal_SE = diagonal_SE[:idx+1]

                    elif (i, j) in diagonal_SW:
                        idx = diagonal_NE.index((i, j))

                        if color == self.owner:
                            diagonal_SW = diagonal_SW[:idx]
                        else:
                            diagonal_SW = diagonal_SW[:idx+1]

                    else:
                        continue

        moveset = diagonal_NE + diagonal_NW + diagonal_SE + diagonal_SW

        return moveset

class GenerateQueenMoveset(object):
    def __init__(self, owner='white'):
        self.owner = owner

        # Initialize Bishop and Rook moveset generator objects
        # The Queen's moveset will simply be an sum of the sets
        # generated by the two objects
        self.rook_moveset_generator(owner=owner)
        self.bishop_moveset_generator(owner=owner)

    def __call__(self, curr_position, board):
        # The queen's moveset is simply a combination of the rook's and the
        # bishop's, so just generate both of those and sum them to create
        # the queen's moveset
        rook_moveset = self.rook_moveset_generator(curr_position, board)
        bishop_moveset = self.bishop_moveset_generator(curr_position, board)

        moveset = bishop_moveset + rook_moveset

        return moveset

class GenerateKnightMoveset(object):
    def __init__(self, owner='white'):
        self.owner = owner

    def __call__(self, curr_position, board, owner="white"):

        (curr_y, curr_x) = curr_position

        # A knight's move is composed of a 2-square move along one axis
        # and a 1-square move along a perpendicular axis

        moveset = [
            (curr_y+2, curr_x+1),
            (curr_y+2, curr_x-1),
            (curr_y+1, curr_x+2),
            (curr_y+1, curr_x-2),
            (curr_y-1, curr_x+2),
            (curr_y-1, curr_x-2),
            (curr_y-2, curr_x+1),
            (curr_y-2, curr_x-1)
        ]

        # Filter for positions off board
        moveset = [(y,x)for (y,x) in moveset if x < _BOARD_WIDTH or x >= 0 \
                         and y < _BOARD_HEIGHT or y >=0]

        # Filter for positions that are occupied by a piece owner by
        # player
        for move in moveset:
            y = move[0]
            x = move[1]

            piece = board[y][x]

            if not piece:
                continue

            (color, _) = piece

            # If the spot is occupied by a piece with the same color
            # as the owner of the knight, remove that move from the
            # generated moveset
            if color == owner:
                moveset.remove(move)

        return moveset

class GeneratePawnMoveset(object):
    def __init__(self,
                 owner='white'):

        self.owner = owner

    def __call__(self, curr_position, board, en_passant=None):
        """
        :param en_passant: Either a tuple with the position
                           of pawn open to en-passant, or
                           a 'None' value if no pawns are open to en-passant
        """

        # A pawn's initial moveset is pretty easy to generate. Just
        # one move forward, except if at starting square,
        # which allows the pawn to move two squares ahead
        (curr_y, curr_x) = curr_position

        if self.owner == 'white' and curr_y == 1:
            moveset = [(curr_y+1, curr_x), (curr_y+2, curr_x)]

        elif self.owner == 'white':
            moveset = [(curr_y+1, curr_x)]

        elif self.owner == 'black' and curr_y == 7:
            moveset = [(curr_y-1, curr_x), (curr_y-2, curr_x)]

        elif self.owner == 'black':
            moveset = [(curr_y-1, curr_x)]

        # Check board to see if there are any possible collisions.
        # Note that if there is an opponent piece at a diagonal,
        # the pawn can move to capture it
        for move in moveset:
            (y, x) = move
            piece = board[y][x]

            if not piece:
                continue
            else:
                moveset.remove(move)

        # Check if there are opponent pieces at diagonals
        if self.owner == 'white':
            y = curr_y + 1
        else:
            y = curr_y - 1

        for x in (-1, 1):
            piece = board[y][x]
            if piece:
                (color, _) = piece
                if color != self.owner:
                    moveset.append((y, x))

        # Check if the pawn can perform an en-passant move
        if en_passant:
            (y, x) = en_passant
            if y == curr_y:
                if x + 1 == curr_x or x - 1 == curr_x:
                    if self.owner == 'white':
                        moveset.append((curr_y+1, x))
                    else:
                        moveset.append((curr_y-1, x))

        return moveset

class GenerateKingMoveset(object):
    def __init__(self, owner='white'):
        self.owner = owner

    def __call__(self,
                 curr_position,
                 board,
                 player_moveset,
                 opponent_moveset):
        """
        :param opponent_moveset: all possible moves the other player's
                                 pieces can make. We need this to verify
                                 that the king can't move to any position
                                 threatened by the other player's pieces
        """
        (curr_y, curr_x) = curr_position

        moveset = [
            (curr_y+1, curr_x),
            (curr_y-1, curr_x),
            (curr_y+1, curr_x+1),
            (curr_y-1, curr_x+1),
            (curr_y+1, curr_x-1),
            (curr_y-1, curr_x-1),
            (curr_y, curr_x+1),
            (curr_y, curr_x-1)
        ]

        # Filter for positions that are being occupied by the player's pieces
        for move in moveset:
            (y, x) = move
            piece = board[y][x]

            if not piece:
                continue

            (color, _) = piece

            if color == self.owner:
                moveset.remove(move)

            # Filter out moves that would place the king in check
            # TODO: put in check that sees if king is being supported
            #       by another piece. If it is, it can move to a position
            #       that would normally be threatened by the opponent king
            #       and, thus, place the opponent's king in check
            if move in opponent_moveset:
                if move not in player_moveset:
                    moveset.remove(move)

        return moveset

