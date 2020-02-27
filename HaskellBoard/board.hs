import Data.Char
import Data.Data
import Data.List
import Prelude

data Color = WHITE | BLACK

data Piece = EMPTY | PAWN | ROOK | KNIGHT | BISHOP | QUEEN | KING

--class Character (Color, Piece) where
--	character :: (Color, Piece) -> String

--instance Character (Color, Piece) where
--	
--    fromEnum (WHITE, EMPTY)  = "\x25f8"
--    fromEnum (WHITE, PAWN)   = "\x265f"
--    fromEnum (WHITE, ROOK)   = "\x265c"
--    fromEnum (WHITE, KNIGHT) = "\x265e"
--    fromEnum (WHITE, BISHOP) = "\x265d"
--    fromEnum (WHITE, QUEEN)  = "\x265b"
--    fromEnum (WHITE, KING)   = "\x265a"	
--    fromEnum (BLACK, EMPTY)  = "\x25Fc"
--    fromEnum (BLACK, PAWN)   = "\x2659"
--    fromEnum (BLACK, ROOK)   = "\x2656"
--    fromEnum (BLACK, KNIGHT) = "\x2658"
--    fromEnum (BLACK, BISHOP) = "\x2657"
--    fromEnum (BLACK, QUEEN)  = "\x2655"
--    fromEnum (BLACK, KING)   = "\x2654"
returnChessChar :: (Color, Piece) -> String
returnChessChar (c, p) | (c, p) == (BLACK, ROOK)    = "\x25f8"
                       | (c, p) == (BLACK, KNIGHT)  = "\x2658"
		       | (c, p) == (BLACK, BISHOP)  = "\x2657"
                       | (c, p) == (BLACK, QUEEN)   = "\x2655"
		       | (c, p) == (BLACK, KING)    = "\x2654"

-- Defining a chess board as a list within list
-- indexed by (row, column)
--let chess_board = [[(BLACK, ROOK), 
--                    (BLACK, KNIGHT),
--                    (BLACK, BISHOP),
--                    (BLACK, QUEEN), 
--                    (BLACK, KING),
--                    (BLACK, BISHOP),
--                    (BLACK, KNIGHT),
--                    (BLACK, ROOK)],
--                   [replicate 8 (BLACK, PAWN)],
--                   replicate 4 [replicate 8 Nothing],
--                   [replicate 8 (WHITE, PAWN)],
--                   [(WHITE, ROOK), 
--                    (WHITE, KNIGHT),
--                    (WHITE, BISHOP),
--                    (WHITE, QUEEN), 
--                    (WHITE, KING),
--                    (WHITE, BISHOP),
--                    (WHITE, KNIGHT),
--                    (WHITE, ROOK)]]

--displayBoard :: [(Color, Piece)] -> IO ()
--displayBoard board = putStr map (map Character reverse board)
--displayCharacter :: (Color, Piece) -> String -> IO ()
--displayCharacter (c, p) = putStr (returnChessChar (c, p))
