import numpy as np

# USER MODULES
from pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King
from display import Color, Characters, PieceDisplay, display_board

ascii_delimiter = 97
HEIGHT = 8
WIDTH = 8

_piece_to_state_representation = {
    'King':   1,
    'Queen':  2,
    'Rook':   3,
    'Bishop': 4,
    'Knight': 5,
    'Pawn':   6,
}

class Board(object):

    def __init__(self,
                 x=8,
                 y=8,
                 human_player=False):

        # Save dimensions of board
        self.width = x
        self.height = y

        # Generate list with all possible 'x-positions'
        x_positions = []
        for i in range(x):
            x_positions.append(chr(ascii_delimiter + i))

        # Generate list with all possible 'y-positions'
        y_positions = list(range(y))

        # Initialize grid
        grid_positions = []
        for x_position in x_positions:
            for y_position in y_positions:
                grid_positions

        # List containing Black pieces still in play
        self.black_pieces_in_play = []
        self.captured_black_pieces = []

        # List containing White pieces still in play
        self.pieces_in_play = {
            'white': [],
            'black': [],
        }
        self.w_king = None
        self.b_king = None

        # Flag for whose turn it is
        # white: 0
        # black: 1
        self.player_flag = 0

        self.checkmate = False

        # seed for numpy random number generator
        self.seed = 1024

    def populate_board(self):
        """
        Initialize board with positions of pieces.
        """
        self.board = [
               [
                   Rook(owner='white', position=(0,0)),
                   Knight(owner='white', position=(1, 0)),
                   Bishop(owner='white', position=(2,0)),
                   Queen(owner='white', position=(3,0)),
                   King(owner='white', position=(4,0)),
                   Bishop(owner='white', position=(5,0)),
                   Knight(owner='white', position=(6,0)),
                   Rook(owner='white', position=(7,0)),
               ],
               [Pawn(owner='white', position=(i,1)) for i in range(8)],
               *[[None] * 8 for _ in range(4)],
               [Pawn(owner='black', position=(i,6)) for i in range(8)],
               [
                   Rook(owner='black', position=(0,7)),
                   Knight(owner='black', position=(1, 7)),
                   Bishop(owner='black', position=(2,7)),
                   Queen(owner='black', position=(3,7)),
                   King(owner='black', position=(4,7)),
                   Bishop(owner='black', position=(5,7)),
                   Knight(owner='black', position=(6,7)),
                   Rook(owner='black', position=(7,7)),
               ],
           ]

        self.display_board = []
        for row in self.board:
            disp_row = []
            for piece in row:
                if piece:
                    disp_row.append(piece.cli_characterset)
                else:
                    disp_row.append(None)
            self.display_board.append(disp_row)


        for i, row in enumerate(self.board):
            self.pieces_in_play['white'].extend([piece for piece in row if i < 2])
            self.pieces_in_play['black'].extend([piece for piece in row if i > 5])

            # Add reference to the kings for both players
            self.w_king = self.board[4][0]
            self.b_king = self.board[4][7]

    def present_movesets(self, turn='white'):
        """
        Analyzes all possible movesets and presents them to player
        """
        pieces_avail = self.pieces_in_play[turn]
        all_possible_moves = []
        for piece in pieces_avail:
            moveset = piece.generate_moveset(self.pieces_in_play)
            all_possible_moves.extend([(piece, move) for move in moveset])

        return all_possible_moves

    def pick_random_move(self, moveset):
        """
        A random move out of possible moveset is chosen
        """
        idx = np.random.random_integers(0, len(moveset))
        return moveset[idx]

    def player_chosen_move(self, moveset):
        """
        Have the player choose a move to take
        """
        choice_idx = ascii_delimiter
        choice_dict = {}
        for (piece, dest_space) in moveset:
            curr_position_in_grid = convert_int_to_grid_coords(piece.position)
            dest_space_in_grid = convert_int_to_grid_coords(dest_space)
            print("{0}) {1} {2} -> {3}".format(chr(choice_idx),
                                               piece.name,
                                               curr_position_in_grid,
                                               dest_space_in_grid))
            choice_dict[chr(choice_idx)] = (piece, dest_space)

        # Have the player choose their move of choice based on index
        while True:
            chosen_idx = input("Which move would you like to choose?")

            try:
                move = choice_dict[chosen_idx.lower()]
            except KeyError:
                print("Error: Input not recognized")
                print("Try Again")

    def one_player_game(self):
        """
        Initialize a game with a human player
        """
        # Have the player choose the color they want to play as
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

        # Populate the board with pieces in their
        # starting positions
        self.populate_board()

        # print initial state of board
        display_board(self.display_board, index=True)

        # Initialize game
        checkmate = False
        turn = None
        while not checkmate:

            # Switch to next player's turn
            if turn == 'white': turn = 'black'
            elif not turn: turn = 'white'
            else: turn = 'white'

            # Switch off the 'two_square_advance' flag for
            # all pieces in play
            for piece in self.pieces_in_play[turn]:
                if piece.name == 'Pawn':
                    self.two_square_advance = False

            movesets = self.present_movesets(turn)

            if player_color == turn:
                (piece, dest_grid_space) = self.player_chosen_move(movesets)
            else:
                (piece, dest_grid_space) = self.pick_random_move(movesets)


            # Check to see if there is an opposing piece at movement position
            # If so, add to list of captured pieces
            if turn == 'white':
                opponent = 'black'
            else:
                opponent = 'white'

            opponent_pieces = self.pieces_in_play[opponent]
            for opp_piece in opponent_pieces:
                if opp_piece.position == dest_grid_space:

                    # Add to captured pieces dict
                    self.captured_pieces[opponent].append(opp_piece)
                    break

            prev_x = piece.position[0]
            prev_y = piece.position[1]

            curr_x = dest_grid_space[0]
            curr_y = dest_grid_space[1]

            # Special logic for pawns: If the pawn moved two spaces from its
            # starting position, it is now vulnerable to en-passant
            if piece.name == 'Pawn':
                piece.two_square_advance = True

            self.board[curr_x][curr_y] = piece
            self.board[prev_x][prev_y] = None

            self.display_board[curr_x][curr_y] = piece.cli_characterset
            self.display_board[prev_x][prev_y] = None

            piece.position = dest_grid_space

            # Print status of board after move
            display_board(self.disp_board, index=True)

            # Generate the new moveset for the moved piece so that we
            # can check whether or not the move places the opposing king
            # in checkmate
            new_moveset = piece.generate_moveset(self.pieces_in_play)

            # Don't need to replace the old moveset for the piece we moved
            # (if that moveset didn't place the King in checkmate before,
            #  it won't now!)
            movesets.append(new_moveset)

            # Check to see if the king of the player whose turn it is
            # has been placed in checkmate
            if turn == 'white': checkmate = self.w_king.check_checkmate(self.pieces_in_play,
                                                                        movesets)
            else: checkmate = self.b_king.check_checkmate(self.pieces_in_play,
                                                          movesets)

        print("Checkmate! {} Has won!".format(turn))
        if turn == player_color: print("Congratulations!")

    def generate_state_of_board(self):
        """
        Initializes vector to feed into DNN based on the state of the board at
        a given moment in time
        """
        state_vector = np.zeros((8,8))
        for i, row in enumerate(self.board):
            for j, grid_space in enumerate(row):
                if grid_space:
                    state_representation = _piece_to_state_representation[grid_space.name]
                    if grid_space.owner == 'black': state_representation = -state_representation
                    state_vector[i][j] = state_representation

        return state_representation

def convert_int_to_grid_coords(int_coords):
    """
    Helper function to convert integer coordinates used internally
    by pieces at play to chess grid coordinates for reference
    """
    # Convert x coord to character using ascii encoding
    x_int_coord = int_coords[0]
    y_int_coord = int_coords[1]
    x_grid_coord = chr(ascii_delimiter + x_int_coord)

    # y coord stays in integer format, so that's easy
    grid_coord = x_grid_coord + chr(y_int_coord)

    return grid_coord

if __name__ == '__main__':
   game_board = Board()
   game_board.one_player_game()
