from moves import *

# Class definition for a chess piece
class piece():
    # Constructor method to initialize the piece attributes
    def __init__(self, piece, color, position, tag="",moved=False,captured=False):
        self.piece = piece  # Type of chess piece ('P', 'B', 'R', 'Q', etc.)
        self.color = color  # Color of the piece ('B' for black, 'W' for white)
        self.moved = moved  # Boolean indicating whether the piece has moved before
        self.position = position  # Current position of the piece on the chessboard
        self.tag = tag  # Additional tag information for the piece
        self.captured = captured  # Boolean indicating whether the piece has been captured
    def score(self):
        """
        this method used to calculate the immediate reward of a move , each peace has a certain
        score to assign importance to it . 
        pawn is worth 1point
        knight is worth 3points
        bishop is worth 3points
        a rook is worth 5points
        a queen is worth 9points
        a king is worth infinity (it doesnt matter as we cannot capture the king )
        """
        if self.piece == "P" : return 2
        if self.piece in ['N','B']:return 5
        if self.piece == 'R' :return 8
        if self.piece == "Q" :return 14
        if self.piece =="K":return 100
    
        return 1

    # Method to determine the possible moves for the piece based on its type and current board configuration
    def possible_moves(self, board):
        square = self.position  # Current position of the piece
        moves = []  # List to store possible moves for the piece
        factor = 1  # Factor to adjust movement direction 

        # Handling possible moves for a pawn
        if self.piece == 'P':
            if self.color == "B":
                factor = -1  # Invert factor for black pawns
            # Check if moving one square forward is a valid move
            if (square[0] + factor) <= 8 and (square[0] + factor)>0 and board[(square[0] + factor, square[1])] == "":
                moves.append((square[0] + factor, square[1]))
            # Check if moving two squares forward is a valid move (only if the pawn hasn't moved yet)
            if not(self.moved):
                if (square[0] + (factor * 2)) <= 8 and (square[0] + (factor * 2)) > 0 and board[(square[0] + 2 * factor, square[1])] == "" and not(self.moved):
                    moves.append((square[0] + factor * 2, square[1]))

            if (square[0]+factor)in range(1,9):
                if (square[1]+1) in range(1,9) and board [( square[0] + factor , square[1]+1)]!="" and board[( square[0] + factor , square[1]+1)].color != self.color :
                    moves.append(( square[0] + factor , square[1]+1))
                if (square[1]-1) in range(1,9) and board [( square[0] + factor , square[1]-1)]!="" and board [( square[0] + factor , square[1]-1)].color != self.color :
                    moves.append(( square[0] + factor , square[1]-1))

            
            return moves

        # Handling possible moves for a bishop
        if self.piece == 'B':
            return diagonal(self, board)

        # Handling possible moves for a rook
        if self.piece == 'R':
            return rook(self, board)

        # Handling possible moves for a queen (combination of rook and bishop moves)
        if self.piece == 'Q':
            return rook(self, board) + diagonal(self, board)
        if self.piece == 'K':
            return king(self,board)
        if self.piece == 'N':
            return knight(self,board)

        return moves  # Return the list of possible moves for the piece
