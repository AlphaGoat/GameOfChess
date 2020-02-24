"""
Classes to define specific pieces on chess board and their movement sets
20 Feb 2020
Peter J. Thomas
"""
import itertools
import pdb

# Custom Modules
from display import Color, PieceDisplay, Characters

HEIGHT = 8
WIDTH = 8


class Piece(object):
    def __init__(self,
                 owner,
                 position):

        # Tuple containing the position of the piece on the board
        self.position = position

        # piece owner
        self.owner = owner

        if self.owner == 'white': self.opponent = 'black'
        else: self.opponent = 'white'

class King(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):

        super().__init__(owner=owner, position=position)
        self.name = 'King'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.KING)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.KING)

    def generate_moveset(self, pieces_in_play, opponent_movesets):
        """
        Generate possible moves for piece
        For King, it's one space in any direction, so long as it's unoccuped
        by a friendly piece and it doesn't put the king in check
        """
        arr_x = [self.position[0], self.position[0] + 1, self.position[0] - 1]
        arr_y = [self.position[1], self.position[1] + 1, self.position[1] - 1]
        moveset = list(itertools.product(arr_x, arr_y))

        # Filter for illegal moves

        # Filter for spots already occuptied by a piece owned by player
        player_piece_coords = pieces_in_play[self.owner]
        moveset = list(filter(lambda x: x != (p_coord for p_coord in player_piece_coords), moveset))

        # Filter spots threatened by the other player's pieces (can't place king in check)
        for (_, threatened_spaces) in opponent_movesets:
            moveset = list(filter(lambda x: x not in threatened_spaces, moveset))

        # Filter for moves outside board space
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 \
                         and pos[1] < HEIGHT and pos[1] >= 0, moveset))

        return moveset

    def check_checkmate(self, pieces_in_play, opponent_movesets):
        """
        Method to check if the king has been placed in checkmate
        """
        # Generate king's moveset. If there are moves available to the king,
        # then he is not in checkmate
        moveset = self.generate_moveset(pieces_in_play, opponent_movesets)
        if not moveset:
            # See if the king is currently being threatened by an opponent's piece
            for (_, threatened_spaces) in opponent_movesets:
                if self.position in threatened_spaces:
                    return True

        return False

class Knight(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):
        super().__init__(owner=owner, position=position)
        self.name = 'Knight'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.KNIGHT)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.KNIGHT)

    def generate_moveset(self,
                         pieces_in_play,
                         ):
        """
        Generate possible moves for piece
        """
        arr_x1 = [self.position[0] + 2, self.position[0] - 2]
        arr_y1 = [self.position[1] + 1, self.position[1] - 1]

        arr_x2 = [self.position[0] + 1, self.position[0] - 1]
        arr_y2 = [self.position[1] + 2, self.position[1] - 2]
        moveset = list(itertools.product(arr_x1, arr_y1)) + list(itertools.product(arr_x2, arr_y2))

        # Filter for illegal moves (For knights, we don't have to account for collision)

        # Filter for moves outside board space
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 \
                              and pos[1] < HEIGHT and pos[1] >= 0, moveset))

        # Filter for spots already occupied by a piece owned by player
        owner_pieces = pieces_in_play[self.owner]

        occupied_player_spaces = [piece.position for piece in owner_pieces]
        moveset = list(filter(lambda pos: pos not in occupied_player_spaces, moveset))

        return moveset

class Bishop(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):
        super().__init__(owner=owner, position=position)
        self.name = 'Bishop'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.BISHOP)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.BISHOP)

    def generate_moveset(self,
                         pieces_in_play,
                         ):
        """
        Generate possible moves for Bishop
        """
        curr_x = self.position[0]
        curr_y = self.position[1]
        arr_x1 = [curr_x + i for i in range(1,8)]
        arr_y1 = [curr_y + i for i in range(1,8)]
        arr_x2 = [curr_x - i for i in range(1,8)]
        arr_y2 = [curr_y - i for i in range(1,8)]

        # Divide moveset into 4-axis of diagonal movement for now (makes later
        # filtering simpler)
        diag1 = list(zip(arr_x1, arr_y1))
        diag2 = list(zip(arr_x1, arr_y2))
        diag3 = list(zip(arr_x2, arr_y1))
        diag4 = list(zip(arr_x2, arr_y2))

        # Filter for illegal moves

        # Filter for positions blocked by other pieces. A piece owned by same player
        # also blocks all positions further down diagonal axis as well
        owner_pieces = pieces_in_play[self.owner]
        grid_coords = [piece.position for piece in owner_pieces]
        for grid_coord in grid_coords:
#            piece_x = player_piece.position[0]
#            piece_y = player_piece.position[1]
#            if abs(piece_x - curr_x) == abs(piece_y - curr_y):
            if grid_coord in diag1:
                idx = diag1.index(grid_coord)
                diag1 = diag1[:idx]
            elif grid_coord in diag2:
                idx = diag2.index(grid_coord)
                diag2 = diag2[:idx]
            elif grid_coord in diag3:
                idx = diag3.index(grid_coord)
                diag3 = diag3[:idx]
            elif grid_coord in diag4:
                idx = diag4.index(grid_coord)
                diag4 = diag4[:idx]

        # Filter for pieces owned by opponent
        # Note that an opponent piece
        # does not prevent a bishop from moving to their position, but  blocks other positions
        # further down its diagonal axis in the moveset
        for opponent_piece in pieces_in_play[self.opponent]:
            if opponent_piece.position in diag1:
                idx = diag1.index(opponent_piece.position)
                diag1 = diag1[:idx+1]
            elif opponent_piece.position in diag2:
                idx = diag2.index(opponent_piece.position)
                diag2 = diag2[:idx+1]
            elif opponent_piece.position in diag3:
                idx = diag3.index(opponent_piece.position)
                diag3 = diag3[:idx+1]
            elif opponent_piece.position in diag4:
                idx = diag4.index(opponent_piece.position)
                diag4 = diag4[:idx+1]

        # Compose moveset from invdividual diagonal axex
        moveset = diag1 + diag2 + diag3 + diag4

        # Filter for moves outside board space
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 \
                         and pos[1] < HEIGHT and pos[1] >= 0, moveset))

        return moveset

class Rook(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):
        super().__init__(owner=owner, position=position)
        self.name = 'Rook'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.ROOK)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.ROOK)

    def generate_moveset(self, pieces_in_play):
        curr_x = self.position[0]
        curr_y = self.position[1]

        arr_x1 = [curr_x + x for x in range(1,8)]
        arr_y1 = [curr_y + y for y in range(1,8)]
        arr_x2 = [curr_x - x for x in range(1,8)]
        arr_y2 = [curr_y - y for y in range(1,8)]

        # Generate seperate movesets for movements along horizontal axes and
        # vertical axes
        hz_axis1 = [(x, curr_y) for x in arr_x1]
        hz_axis2 = [(x, curr_y) for x in arr_x2]
        vt_axis1 = [(curr_x, y) for y in arr_y1]
        vt_axis2 = [(curr_x, y) for y in arr_y2]

        # Check to see if path is blocked by a player piece
        for player_piece in pieces_in_play[self.owner]:
            ppiece_x = player_piece.position[0]
            ppiece_y = player_piece.position[1]

            if ppiece_y == curr_y:
                if (ppiece_x, ppiece_y) in hz_axis1:
                    idx = hz_axis1.index((ppiece_x, ppiece_y))
                    hz_axis1 = hz_axis1[:idx]
                elif (ppiece_x, ppiece_y) in hz_axis2:
                    idx = hz_axis2.index((ppiece_x, ppiece_y))
                    hz_axis2 = hz_axis2[:idx]

            elif ppiece_x == curr_x:
                if (ppiece_x, ppiece_y) in vt_axis1:
                    idx = vt_axis1.index((ppiece_x, ppiece_y))
                    vt_axis1 = vt_axis1[:idx]
                elif (ppiece_x, ppiece_y) in vt_axis2:
                    idx = vt_axis2.index((ppiece_x, ppiece_y))
                    vt_axis2 = vt_axis2[:idx]

        # Check to see if path is blocked by opponent piece. Note that
        # the rook can move to the position of that opponent piece, but
        # not past it
        for opponent_piece in pieces_in_play[self.opponent]:
            opiece_x = opponent_piece.position[0]
            opiece_y = opponent_piece.position[1]

            if opiece_y == curr_y:
                if (opiece_x, opiece_y) in hz_axis1:
                    idx = hz_axis1.index((opiece_x, opiece_y))
                    hz_axis1 = hz_axis1[:(idx+1)]
                elif (opiece_x, opiece_y) in hz_axis2:
                    idx = hz_axis2.index((opiece_x, opiece_y))
                    hz_axis2 = hz_axis2[:(idx+1)]

            elif opiece_x == curr_x:
                if (opiece_x, opiece_y) in vt_axis1:
                    idx = vt_axis1.index((opiece_x, opiece_y))
                    vt_axis1 = vt_axis1[:(idx+1)]
                elif (opiece_x, opiece_y) in vt_axis2:
                    idx = vt_axis2.index((opiece_x, opiece_y))
                    vt_axis2 = vt_axis2[:(idx+1)]

        # Compose moveset from individual axes
        moveset = hz_axis1 + hz_axis2 + vt_axis1 + vt_axis2

        # Filter for moves that would place piece off board
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 \
                          and pos[1] < HEIGHT and pos[1] >= 0, moveset))

        return moveset

class Queen(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):
        super().__init__(owner=owner, position=position)
        self.name = 'Queen'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.QUEEN)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.QUEEN)

    def generate_moveset(self, pieces_in_play):

        curr_x = self.position[0]
        curr_y = self.position[1]

        arr_x1 = [curr_x + i for i in range(1,8)]
        arr_y1 = [curr_y + i for i in range(1,8)]
        arr_x2 = [curr_x - i for i in range(1,8)]
        arr_y2 = [curr_y - i for i in range(1,8)]

        # Divide moveset into 4-axis of diagonal movement for now (makes later
        # filtering simpler)
        diag1 = list(zip(arr_x1, arr_y1))
        diag2 = list(zip(arr_x1, arr_y2))
        diag3 = list(zip(arr_x2, arr_y1))
        diag4 = list(zip(arr_x2, arr_y2))

        # Generate seperate movesets for movements along horizontal axes and
        # vertical axes
        hz_axis1 = [(x, curr_y) for x in arr_x1]
        hz_axis2 = [(x, curr_y) for x in arr_x2]
        vt_axis1 = [(curr_x, y) for y in arr_y1]
        vt_axis2 = [(curr_x, y) for y in arr_y2]


        # Filter for illegal moves

        # Filter for positions blocked by other pieces. A piece owned by same player
        # also blocks all positions further down diagonal axis as well
        for player_piece in pieces_in_play[self.owner]:
            ppiece_x = player_piece.position[0]
            ppiece_y = player_piece.position[1]
#            if abs(piece_x - curr_x) == abs(piece_y - curr_y):

            # Diagonal movesets
            if player_piece.position in diag1:
                idx = diag1.index(player_piece.position)
                diag1 = diag1[:idx]
            elif player_piece.position in diag2:
                idx = diag2.index(player_piece.position)
                diag2 = diag2[:idx]
            elif player_piece.position in diag3:
                idx = diag3.index(player_piece.position)
                diag3 = diag3[:idx]
            elif player_piece.position in diag4:
                idx = diag4.index(player_piece.position)
                diag4 = diag4[:idx]

            elif ppiece_y == curr_y:
                if (ppiece_x, ppiece_y) in hz_axis1:
                    idx = hz_axis1.index((ppiece_x, ppiece_y))
                    hz_axis1 = hz_axis1[:idx]
                elif (ppiece_x, ppiece_y) in hz_axis2:
                    idx = hz_axis2.index((ppiece_x, ppiece_y))
                    hz_axis2 = hz_axis2[:idx]

            elif ppiece_x == curr_x:
                if (ppiece_x, ppiece_y) in vt_axis1:
                    idx = vt_axis1.index((ppiece_x, ppiece_y))
                    vt_axis1 = vt_axis1[:idx]
                elif (ppiece_x, ppiece_y) in vt_axis2:
                    idx = vt_axis2.index((ppiece_x, ppiece_y))
                    vt_axis2 = vt_axis2[:idx]

        # Filter for pieces owned by opponent
        # Note that an opponent piece
        # does not prevent a bishop from moving to their position, but  blocks other positions
        # further down its diagonal axis in the moveset
        for opponent_piece in pieces_in_play[self.opponent]:
            opiece_x = opponent_piece.position[0]
            opiece_y = opponent_piece.position[1]

            # Diagonal movesets
            if opponent_piece.position in diag1:
                idx = diag1.index(opponent_piece.position)
                diag1 = diag1[:idx+1]
            elif opponent_piece.position in diag2:
                idx = diag2.index(opponent_piece.position)
                diag2 = diag2[:idx+1]
            elif opponent_piece.position in diag3:
                idx = diag3.index(opponent_piece.position)
                diag3 = diag3[:idx+1]
            elif opponent_piece.position in diag4:
                idx = diag4.index(player_piece.position)
                diag4 = diag4[:idx+1]

            if opiece_y == curr_y:
                if (opiece_x, opiece_y) in hz_axis1:
                    idx = hz_axis1.index((opiece_x, opiece_y))
                    hz_axis1 = hz_axis1[:(idx+1)]
                elif (opiece_x, opiece_y) in hz_axis2:
                    idx = hz_axis2.index((opiece_x, opiece_y))
                    hz_axis2 = hz_axis2[:(idx+1)]

            elif opiece_x == curr_x:
                if (opiece_x, opiece_y) in vt_axis1:
                    idx = vt_axis1.index((opiece_x, opiece_y))
                    vt_axis1 = vt_axis1[:(idx+1)]
                elif (opiece_x, opiece_y) in vt_axis2:
                    idx = vt_axis2.index((opiece_x, opiece_y))
                    vt_axis2 = vt_axis2[:(idx+1)]

        # Compose moveset from invdividual diagonal axex
        moveset = diag1 + diag2 + diag3 + diag4

        # Compose moveset from individual vertical and horizontal axes
        moveset = moveset + hz_axis1 + hz_axis2 + vt_axis1 + vt_axis2

        # Filter for moves outside board space
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 \
                         and pos[1] < HEIGHT and pos[1] >= 0, moveset))

        return moveset

class Pawn(Piece):
    def __init__(self,
                 owner='white',
                 position=(0,0)):
        super().__init__(owner=owner, position=position)
        self.name = 'Pawn'
        if self.owner == 'white': self.cli_characterset = (Color.WHITE, PieceDisplay.PAWN)
        else: self.cli_characterset = (Color.BLACK, PieceDisplay.PAWN)

        # Pawn requires flag to let players know if it's previous move was
        # advancing two squares from its starting position. This enables
        # an opponent pawn to perform an en-passant capture on it
        self.two_square_advance = False

    def generate_moveset(self, pieces_in_play):
        """
        Generate possible moves for a pawn.
        """
        curr_x = self.position[0]
        curr_y = self.position[1]

        # The movesets generated by white and black pawns will be inverse each other
        # (pawns can only move in one direction)
        if self.owner == 'white':
            # If the pawn is still at the 2nd rank of the board, it can move
            # forward twice
            if curr_y == 1:
                moveset = [
                    (curr_x, curr_y + 1),
                    (curr_x, curr_y + 2)
                ]
            else:
                moveset = [(curr_x, curr_y + 1)]

            # Check to see if there's an opponent piece at a diagonal to the pawn.
            # If so, the pawn can capture it
            for opiece in pieces_in_play[self.opponent]:
                if opiece.position == (curr_x + 1, curr_y + 1) or \
                        opiece.position == (curr_x - 1, curr_y + 1):
                    moveset.append(opiece.position)

                # Is the opponent's piece a pawn, and just moved two
                # spaces from its start? If so, we might be able to
                # capture it en-passant
                if opiece.name == 'Pawn' and opiece.two_square_advance == True:
                    moveset.append((opiece.position[0], curr_y + 1))


        elif self.owner == 'black':
            # If the pawn is still at the 2nd rank of the board, it can move
            # forward twice
            if curr_y == 6:
                moveset = [
                    (curr_x, curr_y - 1),
                    (curr_x, curr_y - 2)
                ]
            else:
                moveset = [(curr_x, curr_y -1)]

            # Check to see if there's an opponent piece at a diagonal to the pawn.
            # If so, the pawn can capture it
            for opiece in pieces_in_play[self.opponent]:
                if opiece.position == (curr_x + 1, curr_y - 1) or \
                        opiece.position == (curr_x - 1, curr_y - 1):
                    moveset.append(opiece.position)

                # Is the opponent's piece a pawn, and just moved two
                # spaces from its start? If so, we might be able to
                # capture it en-passant
                if opiece.name == 'Pawn' and opiece.two_square_advance == True:
                    moveset.append((opiece.position[0], curr_y - 1))

        # Check to see if a piece owned by the player is blocking the path
        # of the pawn
        for ppiece in pieces_in_play[self.owner]:
            if ppiece.position in moveset:
                idx = moveset.index(ppiece.position)
                moveset.pop(idx)

        # Check to see if a piece owned by the opponent is blocking the
        # path of the pawn
        for opiece in pieces_in_play[self.opponent]:
            if opiece.position in moveset:
                idx = moveset.index(opiece.position)
                moveset.pop(idx)

        # Filter for moves outside board space
        moveset = list(filter(lambda pos: pos[0] < WIDTH and pos[0] >= 0 and \
                         pos[1] < HEIGHT and pos[1] >= 0, moveset))

        return moveset

if __name__ == '__main__':

    w_rook = Rook(owner='white',
                  position=(3,3))

    bk_knight = Knight(owner='black',
                       position=(2,1))

    bk_queen = Queen(owner='black',
                     position=(3,4))

    pieces_in_play = {
        'white': [
            w_rook,
        ],
        'black': [
            bk_knight,
            bk_queen,
        ]
    }

    moveset = bk_queen.generate_moveset(pieces_in_play)

    print("moveset: ", moveset)





