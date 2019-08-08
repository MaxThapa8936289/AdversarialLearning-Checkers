import board as board
import player
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import time

# Game Class for Checkers game
#   Will host two player classes and store the game board history. Will provide
#   a space within which the players can pass boards (i.e. moves) back and 
#   forth.
# Plan: 
# Game Class
# Properties:   Players, Boards
#
# Initialisers: players
#

GAME = True
DELAY = 0
TURNS = 150


class Game:
    def __init__(self,P1=player.Player(delay=DELAY,agent="minimax"),P2=player.Player(delay=DELAY,agent="minimax"),start_pos=board.START_POS):
        self.P1 = P1
        self.P2 = P2
        self.current_board = board.Board(start_pos,show=True)
        self.board_history = [copy(self.current_board)]
    
    def play(self):
        finished = False
        current_player = self.P1
        counter = 0
        start_time = time.time()
#        print(self.P1.coeff)
        learners = []
        for p in [self.P1,self.P2]:
            if p.agent == "TDLearning":
                learners.append(p)
        while GAME is not finished:
            # ## Functionality ##
            #
            # If it's black's turn
            #   player 1 makes the move
            # If its red's turn
            #   player 2 makes the move
            # obtain the new state from the selected move
            # record the new state
            # If there are any learning agents
            #   for each one
            #       update the weights based on the new state and the 
            #       prediction of the old state.
            #
            # if the game has reached the limit for turns
            #   call it a draw
            # if the game has been won (new state has no available moves)
            #   it's a win for the player that just moved.
            # 
            # update the 'current' state, ready for the next iteration
            # add 1 to the turn count

            if self.current_board.turn == board.BLACK:
                current_player = self.P1
            elif self.current_board.turn == board.RED:
                current_player = self.P2                
            new_board = current_player.makeMove(self.current_board)
            self.board_history.append(new_board)
            
            if learners:
                for learner in learners:
                    learner.updateWeightsWithTDLearning(self.current_board,
                                                        new_board)
                            
            if counter == TURNS: # draw
                finished = True
                winner = "DRAW"
                print("DRAW")
                print("Game length: %r turns over %.5f seconds" % (counter, (time.time() - start_time)))
            elif new_board.availableMoves.size == 0: # game won
                finished = True
                winner = board.turn_to_string(self.current_board.turn)
                print("%s wins!" % winner)
                print("Game length: %r turns over %.5f seconds" % (counter, (time.time() - start_time)))
            else:
                self.current_board = copy(new_board)
                counter += 1
        return winner

np.set_printoptions(linewidth=200,precision=2)

P1 = player.Player(delay=DELAY,agent="TDLearning")
P2 = player.Player(delay=DELAY,agent="alphaBeta")
wins_list = []
for i in range(0,1):
    g = Game(P1=P1,P2=P2)
    wins_list.append(g.play())
#learned_params = np.append(P1.eta_updates,P1.coeff)
#np.savetxt('TD_coeff.txt',learned_params,delimiter=',')


# Kowalski, analysis
plt.figure(1)

blk = wins_list.count("BLACK")
red = wins_list.count("RED")
draw = wins_list.count("DRAW")
x = ["Black","Red","Draw"]
y = [blk,red,draw]

plt.bar(x,y)
plt.xlabel('Winning Player')
plt.ylabel('Win Frequency')


plt.figure(2)
function_names = []
for function in board.CBBFunc.getFunctionList():
    function_names.append(board.f.extractFunctionNameFromStrPointer(str(function)))
weights = P1.coeff
plt.title("Player 1: Parameters")
plt.bar(function_names,weights)
plt.xticks(rotation='vertical')
plt.xlabel('Feature Scores')
plt.ylabel('Weight')

plt.figure(3)
function_names = []
for function in board.CBBFunc.getFunctionList():
    function_names.append(board.f.extractFunctionNameFromStrPointer(str(function)))
weights = P2.coeff
plt.title("Player 2: Parameters")
plt.bar(function_names,weights)
plt.xticks(rotation='vertical')
plt.xlabel('Feature Scores')
plt.ylabel('Weight')


plt.show()
np.set_printoptions(precision=None,linewidth=None)