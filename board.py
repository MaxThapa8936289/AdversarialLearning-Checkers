import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from copy import copy
import functions as f
import checkersBitBoardFunctions as CBBFunc

# Board Class for Checkers game
# 
# Plan:
# Board Class
# Properties:   list of Available moves, list of Available move scores, 
#               record of Piece advantage
# Initialisers: Default is game start
#               can take any board position as input.
# Functions:    Display Board, Make move


###############################################################################
# The Game of Checkers ########################################################
###############################################################################
# A standard checkers board consists of an 8x8 board of black and white squares.
# Only the black squares are used in the game. The standard setup for the game 
# start is shown below, with '.' representing the white unusable squares, 
# 'R' representing the Red player's pieces, 'B' representing the Black 
# player's pieces and '_' representing the usable but empty squares.
#                      . R . R . R . R
#                      R . R . R . R .
#                      . R . R . R . R
#                      _ . _ . _ . _ .
#                      . _ . _ . _ . _
#                      B . B . B . B .
#                      . B . B . B . B
#                      B . B . B . B .
# Pieces nominally move by advancing in the direction of the opposite wall. 
# This is achieved with a sliding motion to a diagonally adjacent empty 
# square. If a peice reaches the opposite end of the board, it is 'crowned'
# and becomes a 'king' piece. Kings may move backward as well as forward, i.e.
# they can slide or jump in any of the four diagonal directions available to it. 
# Enemy pieces can be 'captured' via a special motion called a jump.
# In this motion, a player's piece will jump over an enemy piece in a 
# diagonally adjacent square and land in an empty square just beyond.
#
#       _ . _ . _       _ . _ . _      
#       . _ . _ .       . _ . B .
#       _ . R . _  ->   _ . _ . _
#       . B . _ .       . _ . _ .
#
# Once a player completes a move, they may make another jump with the same 
# piece, if one is available. This is repeated until there are no more jumps 
# to make. 
# During play, players take turns moving pieces in a legal manner. Players are
# forced to make a jump move if any are available. If and only if none are
# available are they allowed to make a slide move.
#
# For communication purposes, a labelling convention of the tiles is introduced.
# The usable squares are numbered by counting from 32 down to 1 following 
# a reading-like motion.
#                      . 32 . 31 . 30 . 29
#                      28 . 27 . 26 . 25 .
#                      . 24 . 23 . 22 . 21
#                      20 . 19 . 18 . 17 .
#                      . 16 . 15 . 14 . 13
#                      12 . 11 . 10 . 09 .
#                      . 08 . 07 . 06 . 05
#                      04 . 03 . 02 . 01 .
# There will be other labelling conventions introduced later. It is therefore
# appropriate to name the above convention. We will call it the 'Reading
# Convention' or, more commmonly, just 'R'.

# Colour map for board display, from left to right:
# Pink=RedKings, Red=RedMen, LightGrey=Empty, Black=BlackMen, Grey=BlackKings
cmap = ListedColormap(['#e04b35','#c41900','#f2f2f2','k','#424242'])
# A matrix of R-convention numbers for the graphical display of the board
R_number_matrix = []
for n in range(0,32):
    R_number_matrix.append(str(32-n))
    R_number_matrix.append('')
R_number_matrix = np.array(R_number_matrix)    
R_number_matrix = R_number_matrix.reshape(8,8) # reshape 1x64 to 8x8
R_number_matrix[::2] = np.roll(R_number_matrix[::2],1,axis=1) # apply checkering

###############################################################################                      
# Pragramming Labelling Convention ############################################
###############################################################################
# Since only half the board is used, the gamespace can be reduced by a factor 
# of two from 8x8 = 64 down to 32. We have already seen this with the Reading 
# Convention for labelling squares.
# Often when interacting with the board state, we will need to calculate the 
# legal moves. If we inspect all the left-forward-slide moves from the first 
# row to the second row are: [1,6], [2,7] and [3,8] it is easy to observe that
# the function [initial square] + 5 = [final square] represents the a 
# left-forward-slide move.
# However, the alternation of the squares mean that left-forward-slide moves 
# from the second row to the third row follow the function
# [initial square] + 4 = [final square].
# Rather than program exceptions for each alternating row, it is convenient
# to restore symmetry by using a different standard for labelling squares.
# This convention adds three "imaginary" squares that are labelled but never
# used in play.
#                      . 35 . 34 . 33 . 32
#                      31 . 30 . 29 . 28 . *27
#                      . 26 . 25 . 24 . 23
#                      22 . 21 . 10 . 19 . *18
#                      . 17 . 16 . 15 . 14
#                      13 . 12 . 11 . 10 . *09
#                      . 08 . 07 . 06 . 05
#                      04 . 03 . 02 . 01 . 
# Now it is easy to see that all left-forward-slide moves follow the same 
# function regardless of the initial square chosen. Furthermore, functions that 
# would have previously caused problems such as (5 + 4) or (8 + 5) now map onto 
# those 'imaginary' squares and thus can be error handled in a simple and 
# unified manner.
# This convention is exceptionally useful for programming and algorithm design, 
# and so we will call it the 'Programming Convention", or just 'P.
# It will be used for the majority of this program though, when required, 
# we will convert from P to R for the front end user.

###############################################################################
# Position Array Constants ####################################################
###############################################################################
# The position of pieces will be represented as a single numpy array of 
# integers, in the range[-2,-1,0,1,2], where negative integers are the enemy
# pieces, postive integeers are the allied pieces and zeros are empty squares.
# Integers of magnitude 1 and 2 are the pieces of type man and king,
# respectively. The imaginary squares will always be '0'.

# START_POS is the initial loctions of all pieces in a normal game.
START_POS =          np.array([  -1,   -1,   -1,   -1,
                              -1,   -1,   -1,   -1,    0,
                                 -1,   -1,   -1,   -1,
                               0,   0,    0,    0,     0,
                                  0,    0,    0,    0,
                               1,    1,    1,    1,    0,
                                  1,    1,    1,    1,
                               1,    1,    1,    1     ])
# JUMP_TEST is for debugging jumping behaviour.
JUMP_TEST =         np.array([   -1,    0,    0,    0,
                              -1,   -1,   -1,   -1,    0,
                                  0,    0,    0,   -1,
                               0,   -1,    0,   -1,    0,
                                  0,    1,    0,   -1,
                               1,    0,   -1,    1,    0,
                                  1,    1,    1,    1,
                               1,    0,    1,    1     ])
# END_TEST is for debugging game end behaviour.
END_TEST =          np.array([   0,    0,    0,    0,
                               0,    0,    0,    0,    0,
                                  0,    0,    0,    0,
                               0,   -1,    0,   -1,    0,
                                  0,    0,    0,    0,
                               0,    0,    1,    0,    0,
                                  0,    0,    0,    0,
                               0,    0,    0,    0     ])




# The side who's turn it is is represented by either a 1 or a -1 which helps 
# with calculations. For the benefit of making the code more readable, these
# constants are used in the code.
BLACK = 1
RED = -1

def turn_to_string(turn):
    """ Converts a turn constant to a string.
    >>> BLACK
    1
    >>> turn_to_string(BLACK)
    'BLACK'
    """
    if turn == BLACK:
        return "BLACK"
    elif turn == RED:
        return "RED"
    else:
        raise ValueError("Failed to match argument to turn constant RED = -1 or BLACK = 1")

def is_square(sq):
    """ Checks if square exists on the board (P-convention) """
    if (sq > 0) and (sq < 36) and (sq%9 != 0):
        return True
    else: 
        return False

# KINGS_ROW are the P-conventions squares of the king's row for each player
# used in move() for identifying a crowning event.
KINGS_ROW = {BLACK:(35,34,33,32), RED:(4,3,2,1)}

def move(board,move,show=False):
    """ Returns a new board object after making the move on the given board
    board (Board object) - the board sate to be operated on
    move (np.array or list, 2 integer elements only) - the move to be made from
        square move[0] to square move[1], numbers in P-convention.
    show (boolean) - True: display the result of the movement by calling
        display() on the new Board object.
    
    Functionality:
    If move is legal slide move
      perform move
      return new board
    Else if move is a legal jump
      perform jump
      If there are further jumps to make
          it remains the player's turn
          and only connected jumps will be available
      Else turn goes to the opponent
      return new board
    Else
      move must be illegal
      print error message
      return origonal board
    
    Notes: The P-convention of labelling is the reverse to the indicies of 
    the pos array, therefore the correct element can be indexed with the
    negative of the desired square. 
    >>> P-Labels = [35,34,33,32,...,3,2,1]
    >>> P-Labels[-33] 
    33
    """
    
    assert (not isinstance(move,str) and len(move) == 2), \
    "%r is not a move doublet" % move
    
    if (f.rowIn2dMatrix(board.simpleMoves,move) and board.jumps.size == 0):
        new_pos = copy(board.pos)
        new_pos[-move[0]] = 0
        if (board.is_king_ally(move[0]) or move[1] in KINGS_ROW[board.turn]):
            # assign the new position the piece type
            # multiply by turn to get the correct colour.
            new_pos[-move[1]] = 2*board.turn 
        else:
            new_pos[-move[1]] = 1*board.turn
        new_board = Board(new_pos,turn=-1*board.turn,show=False)
        if show==True:
            new_board.display()
        return new_board
    elif (f.rowIn2dMatrix(board.jumps,move) and f.rowIn2dMatrix(board.availableMoves,move)):
        new_pos = np.array(board.pos)
        captured = int((move[0] + move[1])/2)
        new_pos[-move[0]] = 0
        new_pos[-captured] = 0
        if (board.is_king_ally(move[0])):
            new_pos[-move[1]] = 2*board.turn
            crowning_event = False
        elif (board.is_man_ally(move[0]) and move[1] in KINGS_ROW[board.turn]):
            new_pos[-move[1]] = 2*board.turn
            crowning_event = True
        else:
            new_pos[-move[1]] = 1*board.turn
            crowning_event = False
    
        new_board = Board(new_pos,turn=board.turn,show=False)
        if (new_board.jumps.size != 0 and (move[1] in new_board.jumps[:,0]) and (not crowning_event)):
            new_board.availableMoves = \
            new_board.jumps[tuple([move[1] == new_board.jumps[:,0]])]
        else:
            new_board = Board(new_pos,turn=-1*board.turn,show=False)
        if show==True:
            new_board.display()
        return new_board
    else:
        print("Move is illegal. No move has been made.")
        return board
    
###############################################################################
# The 'Board' State Object ####################################################
###############################################################################
# The agent I wish to build uses a type of MDP learning called
# Time Differential Learning or TD-Learning for short. This agent requires 
# knowledge of a state, and the possible transitions to another state. Under 
# this model, the state strictly contains all information required to choose 
# the optimal transistion, though calculating which transition that may be is 
# not trivial.
# The transitions are simply the legal moves avaialable from a state, 
# while the state is the position of all of the peices at any particular 
# instance during play.
# The Board state I have built in this program contains:
# - the layout of the peices on the board
# - the current turn
# - the avaialable transitions
# - functions to calculate or access the above information
# - a function to display the above information graphically
# - a function to approximate the value of the state.
        
class Board:
    """ Represents a Checkers board in a particular state of play.
    
    Stores the piece positions as both an ndarray and as a binary string.
    Calcualtes possible moves from the state.
    
    Attributes
    ----------
    pos : 1D numpy.ndarray (int)
        Array of length 35 containing non-zero integers at the positions 
        corresponding to the positions of squares on the board 
        (P-Convention). Integers 1 and 2 correspond to pieces of type man 
        and king, respectively. Positive integers correspond to black pieces,
        negative integers are red pieces. 0s are empty tiles. 
    turn : int, either 1 or -1
        Integer representing which colour's turn is currently in play.
        1 corresponds to black's turn. -1 corresponds to red's turn.
    simpleMoves : 2D numpy.ndarray (int)
        Pairs of integers corresponding to the moves that can be made by 
        moving a piece to a diagonally adjacent empty tile (P-Convention). 
    jumps : 2D numpy.ndarray (int)
        Pairs of integers corresponding to the moves that can be made by 
        capturing an enemy piece (P-Convention). 
    available_moves : 2D numpy.ndarray (int)
        Pairs of integers corresponding to the moves that can
        be made by during the current state of play, according to the rules of
        checkers. 
        
    """
    
    def __init__(self,pos=START_POS,turn=BLACK,show=False):
        """ Initialises a Board object representing a checkers board and the 
        pieces in play.

        Parameters
        ----------
        pos : 1D numpy.ndarray (int); optional
            Array of length 35 containing non-zero integers at the positions 
            corresponding to the positions of squares on the board 
            (P-Convention). Integers 1 and 2 correspond to pieces of type man 
            and king, respectively. Positive integers correspond to black pieces,
            negative integers are red pieces. 0s are empty tiles.
            The default is START_POS, the starting layout for a standard game.
        turn : int, either 1 or -1; optional
            Integer representing which colour's turn is currently in play.
            1 corresponds to black's turn. -1 corresponds to red's turn. 
            The default is 1.
        show : BOOL, optional
            If True, calls self.display() on object creation. 
            The default is False.

        Returns
        -------
        None.

        """
            
        self.pos = copy(pos)
        self.turn = turn
        self.simpleMoves, self.jumps = self._getMoves()
        if self.jumps.size != 0:
            self.availableMoves = copy(self.jumps)
        else:
            self.availableMoves = copy(self.simpleMoves)
        if show:
            self.display()
        
        # Positions in binary representation
        if turn == RED:
            relative_pos = np.flip(pos) 
        if turn == BLACK:
            relative_pos = pos
        self.allied_men = CBBFunc.boolPos2ToBin(relative_pos==1*self.turn)
        self.allied_kings = CBBFunc.boolPos2ToBin(relative_pos==2*self.turn)
        self.allies = self.allied_men | self.allied_kings
        
        self.enemy_men = CBBFunc.boolPos2ToBin(relative_pos==-1*self.turn)
        self.enemy_kings = CBBFunc.boolPos2ToBin(relative_pos==-2*self.turn)
        self.enemies = self.enemy_men | self.enemy_kings
        
        self.empty = CBBFunc.NOT35bit(self.allies | self.enemies) & CBBFunc.SQRS
    
    def getSimpleMoves(self):
        return copy(self.simpleMoves)
    def getJumps(self):
        return copy(self.jumps)
    def getAvailableMoves(self):
        return copy(self.availableMoves)
    def getTurn(self):
        return copy(self.turn)
    
    def display(self,trueNums=False,showMoves=False):
        """ Generates a graphical representation of the board and plots it.

        Parameters
        ----------
        trueNums : BOOL, optional
            Debugging tool - prints the integer pieces on the board.
            The default is False.
        showMoves : BOOL, optional
            Prints the list of moves for the current state to the console. 
            The default is False.

        Returns
        -------
        None.

        """
        temp = f.posArrayToReadArray(self.pos)
        disp = np.zeros((64), dtype=np.int32)
        disp[::2] = temp
        disp = disp.reshape(8,8)
        disp[::2] = np.roll(disp[::2],1,axis=1)
        if trueNums:
            print(disp*self.turn)
        else:
            plt.matshow(disp, cmap = cmap, vmin = -2, vmax = +2)
            for (i, j), z in np.ndenumerate(R_number_matrix):
                plt.text(j, i, z, ha='center', va='center', color='#c7c7c7')
            plt.show()
            print('\n')
            print("%s's turn" % turn_to_string(self.turn))
            if showMoves:
                print("Moves available for this turn: ")
                print(self.availableMoves)
                print("All moves including illegal ones: ")
                print(self.simpleMoves)
                print(self.jumps)
        
    def occupation_of(self, sq):
        if is_square(sq):
            return self.pos[-sq]
        else:
            raise ValueError("Argument not a square")
    def is_empty(self,sq):
        return self.occupation_of(sq) in [0]
    def is_enemy(self,sq):
        return self.occupation_of(sq) in [x*self.turn for x in [-1,-2]]
    def is_ally(self,sq):
        return self.occupation_of(sq) in [x*self.turn for x in [1,2]]
    def is_king_ally(self,sq):
        return self.occupation_of(sq) in [2*self.turn]
    def is_man_ally(self,sq):
        return self.occupation_of(sq) in [1*self.turn]
        
    def _getMoves(self):
        """ Calculates all moves that can be made by the current turn.
        
        Simple moves and jumps (i.e captures) are both calculated regardless 
        of legality (this is required for feature evaluation).


        Returns
        -------
        tuple, length 2
            Tuple containing 2 elements which are both ndarrays:
            the simple moves and the jumps.

        """
        
        moves = []
        jumps = []
        # Get a list of squares occupied by men and kings
        men = 35 - np.flatnonzero(self.pos == 1*self.turn)
        kings = 35 - np.flatnonzero(self.pos == 2*self.turn)
        for m in men:
            for _,right_left in f.range_of_man(m,piece_colour=self.turn).items():
                if is_square(right_left["slide"]):
                    if self.is_empty(right_left["slide"]):
                        moves.append([m,right_left["slide"]])
                    elif (self.is_enemy(right_left["slide"])
                            and is_square(right_left["jump"])
                            and self.is_empty(right_left["jump"])):
                        jumps.append([m,right_left["jump"]])
        for k in kings:
            for _,forward_backward in f.range_of_king(k).items():
                for _,right_left in forward_backward.items():
                    if is_square(right_left["slide"]):
                        if self.is_empty(right_left["slide"]):
                            moves.append([k,right_left["slide"]])
                        elif (self.is_enemy(right_left["slide"])
                                and is_square(right_left["jump"])
                                and self.is_empty(right_left["jump"])):
                            jumps.append([k,right_left["jump"]])
        return (np.array(moves),np.array(jumps))

    def feature_score(self, coeff):
        """ Returns the feature score of the state given a weight vector """
        return CBBFunc.calculateFeatureScore(self,coeff)
    
    
    
            
                
        
       
