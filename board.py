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

# Colour map for board display
cmap = ListedColormap(['#e04b35','#c41900','#f2f2f2','k','#424242'])
# Square numbers for board display 
square_numbers = []
for n in range(0,32):
    square_numbers.append(str(32-n))
    square_numbers.append('')
square_numbers = np.array(square_numbers)    
square_numbers = square_numbers.reshape(8,8)
square_numbers[::2] = np.roll(square_numbers[::2],1,axis=1)
                       
# Default position array
START_POS = np.array([-1,-1,-1,-1,
                      -1,-1,-1,-1,
                      -1,-1,-1,-1,
                      0,0,0,0,
                      0,0,0,0,
                      1,1,1,1,
                      1,1,1,1,
                      1,1,1,1,])
# alterantive position array to test move mechanics
JUMP_TEST = np.array([-1,0,0,0,
                      -1,-1,-1,-1,
                      0,0,0,-1,
                      0,-1,0,-1,
                      0,1,0,-1,
                      1,0,-1,1,
                      1,1,1,1,
                      1,0,1,1])
JUMP_TEST2 = np.array([0,0,0,0,
                      0,0,0,0,
                      0,0,2,0,
                      0,0,-1,0,
                      0,0,0,0,
                      0,0,0,0,
                      -2,0,-1,0,
                      0,0,0,0])
MINIMAX_TEST = np.array([0,-1,0,0,
                      0,0,0,0,
                      0,-1,-1,0,
                      0,0,0,0,
                      0,0,0,0,
                      0,1,0,0,
                      0,0,0,0,
                      1,0,0,0])
MINIMAX_TEST2 = np.array([-1,-1,-1,-1,
                          -1,-1,0,0,
                          0,0,-1,-1,
                          0,0,0,0,
                          0,0,1,0,
                          -1,1,-1,1,
                          1,1,0,0,
                          1,1,0,0])

# turn constants
BLACK = 1
RED = -1

# positional constants
SQUARES = np.array([s for s in range (35,-1,-1) if s%9 !=0]) # index of squares
KINGS_ROW = {BLACK:SQUARES[:4], RED:SQUARES[28:]}   

def turn_to_string(turn):
    """ Converts a turn constant to a string """
    if turn == BLACK:
        return "BLACK"
    elif turn == RED:
        return "RED"
    else:
        raise ValueError("Failed to match argument to turn constant RED or BLACK")
                       
def is_square(sq):
    """ Checks if square exists on board """
    if sq in SQUARES: 
        return True
    else: 
        return False

#DEPRECIATED
#def simpleMove(board,move):
#    """ Return a new board in which the move has been made on the given board 
#    """
#    assert not isinstance(move,str), "%r is not a move tuple" % move
#    assert move in board.availableMoves, "%r is not an available move" % move
#    #assert self.jumps.size == 0, "Cannot perform simple move %r when jump is available" % move
#    new_pos = np.array(board.pos)
#    new_pos[SQUARES == move[0]] = 0
#    if (board.is_king_ally(move[0]) or move[1] in KINGS_ROW[board.turn]):
#        new_pos[SQUARES == move[1]] = 2
#    else:
#        new_pos[SQUARES == move[1]] = 1
#    new_board = Board(new_pos,turn=-1*board.turn,changing_sides=True)
#    return new_board
#
#def jump(board,jump):
#    """ Return a new board in which the jump has been made on the given board
#    """
#    assert not isinstance(jump,str), "%r is not a move tuple" % jump
#    assert jump in board.availableMoves, "%r is not an available jump" % jump
#    new_pos = np.array(board.pos)
#    captured = (jump[0] + jump[1])/2
#    new_pos[SQUARES == jump[0]] = 0
#    new_pos[SQUARES == captured] = 0
#    if (board.is_king_ally(jump[0]) or jump[1] in KINGS_ROW[board.turn]):
#        new_pos[SQUARES == jump[1]] = 2
#    else:
#        new_pos[SQUARES == jump[1]] = 1
#
#    new_board = Board(new_pos,turn=board.turn,changing_sides=False,show=False)
#    if (new_board.jumps.size != 0 and (jump[1] in new_board.jumps[:,0])):
#        new_board.availableMoves = \
#        new_board.jumps[tuple([jump[1] == new_board.jumps[:,0]])]
#    else:
#        new_board = Board(new_pos,turn=-1*board.turn,changing_sides=True,show=False)
#    new_board.display()
#    return new_board


def move(board,move,show=True):
    """ Returns a new board object after making the move on the given board
    """
    # Functionality:
    # If move is legal move
    #   perform move
    #   return new board
    # Else if move is a legal jump
    #   perform jump
    #   if there are further jumps to make
    #       it remains the player's turn
    #       and only connected jumps will be available
    #   else turn goes to the opponent
    #   return new board
    # Else
    #   move must be illegal
    #   print error message
    #   return origonal board
    
    assert (not isinstance(move,str) and len(move) == 2), \
    "%r is not a move 2-tuple" % move
    
    if (move in board.simpleMoves and board.jumps.size == 0):
        new_pos = np.array(board.pos)
        new_pos[SQUARES == move[0]] = 0
        if (board.is_king_ally(move[0]) or move[1] in KINGS_ROW[board.turn]):
            new_pos[SQUARES == move[1]] = 2
        else:
            new_pos[SQUARES == move[1]] = 1
        new_board = Board(new_pos,turn=-1*board.turn,changing_sides=True,show=False)
        if show==True:
            new_board.display()
        return new_board
    elif (move in board.jumps and move in board.availableMoves):
        new_pos = np.array(board.pos)
        captured = (move[0] + move[1])/2
        new_pos[SQUARES == move[0]] = 0
        new_pos[SQUARES == captured] = 0
        if (board.is_king_ally(move[0])):
            new_pos[SQUARES == move[1]] = 2
            crowning_event = False
        elif (board.is_man_ally(move[0]) and move[1] in KINGS_ROW[board.turn]):
            new_pos[SQUARES == move[1]] = 2
            crowning_event = True
        else:
            new_pos[SQUARES == move[1]] = 1
            crowning_event = False
    
        new_board = Board(new_pos,turn=board.turn,changing_sides=False,show=False)
        if (new_board.jumps.size != 0 and (move[1] in new_board.jumps[:,0]) and (not crowning_event)):
            new_board.availableMoves = \
            new_board.jumps[tuple([move[1] == new_board.jumps[:,0]])]
        else:
            new_board = Board(new_pos,turn=-1*board.turn,changing_sides=True,show=False)
        if show==True:
            new_board.display()
        return new_board
    else:
        print("Move is illegal. No move has been made.")
        return board
    
class Board:
    def __init__(self,pos=START_POS,turn=BLACK,changing_sides=False,show=False):
        self.pos = np.array(pos)
        self.turn = turn
        if changing_sides:
            self.change_sides()
        self.simpleMoves, self.jumps = self._getMoves()
        if self.jumps.size != 0:
            self.availableMoves = copy(self.jumps)
        else:
            self.availableMoves = copy(self.simpleMoves)
        if show:
            self.display()
        
        # positions in binary arrays
        if turn == RED:
            relative_pos = np.flip(pos) 
        if turn == BLACK:
            relative_pos = pos
        self.allied_men = CBBFunc.boolPosToBin(relative_pos==1)
        self.allied_kings = CBBFunc.boolPosToBin(relative_pos==2)
        self.allies = self.allied_men | self.allied_kings
        
        self.enemy_men = CBBFunc.boolPosToBin(relative_pos==-1)
        self.enemy_kings = CBBFunc.boolPosToBin(relative_pos==-2)
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
        # Displays the board and the available moves
        temp = self.pos*self.turn
        disp = np.zeros((64), dtype=np.int32)
        disp[::2] = temp
        disp = disp.reshape(8,8)
        disp[::2] = np.roll(disp[::2],1,axis=1)
        if trueNums:
            print(disp*self.turn)
        else:
            plt.matshow(disp, cmap = cmap, vmin = -2, vmax = +2)
            for (i, j), z in np.ndenumerate(square_numbers):
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
            
    def change_sides(self):
        self.pos = -1*self.pos
        
    def occupation_of(self, sq):
        return self.pos[SQUARES == sq]
    def is_empty(self,sq):
        return self.occupation_of(sq) in [0]
    def is_enemy(self,sq):
        return self.occupation_of(sq) in [-1,-2]
    def is_ally(self,sq):
        return self.occupation_of(sq) in [1,2]
    def is_king_ally(self,sq):
        return self.occupation_of(sq) in [2]
    def is_man_ally(self,sq):
        return self.occupation_of(sq) in [1]
        
    def _getMoves(self):
        # Returns list of move tuples
        moves = []
        jumps = []
        men = SQUARES[self.pos == 1]
        kings = SQUARES[self.pos == 2]
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
        return CBBFunc.calculateFeatureScore(self,coeff)
    
    
    
            
                
        
       
