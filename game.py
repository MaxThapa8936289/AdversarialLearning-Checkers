import board
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
DELAY = 2
TURNS = 100


class Game:
    def __init__(self,P1=player.Player(delay=DELAY,agent="minimax"),P2=player.Player(delay=DELAY,agent="minimax"),start_pos=board.START_POS):
        self.P1 = P1
        self.P2 = P2
        self.current_board = board.Board(start_pos)
        self.board_history = []
    
    def play(self):
        finished = False
        turn = board.BLACK
        current_player = self.P1
        counter = 0
        start_time = time.time()
        print(self.P1.coeff)
        while GAME is not finished:
            self.board_history.append(self.current_board)
            if turn == board.BLACK:
                current_player = self.P1
            elif turn == board.RED:
                current_player = self.P2                
            new_board = current_player.makeMove(self.current_board)
            turn = new_board.getTurn()

            self.current_board = copy(new_board)
            if counter == TURNS:
                finished = True
                winner = "DRAW"
                print("DRAW")
                print("Game length: %r turns over %.5f seconds" % (counter, (time.time() - start_time)))
            elif self.current_board.availableMoves.size == 0:
                finished = True
                winner = board.turn_to_string(self.board_history[-1].turn)
                print("%s wins!" % winner)
                print("Game length: %r turns over %.5f seconds" % (counter, (time.time() - start_time)))
            counter += 1
        return winner

np.set_printoptions(linewidth=200,precision=2)

P1 = player.Player(delay=DELAY,agent="TDLearning")
P2 = player.Player(delay=DELAY,agent="alphaBeta")
wins_list = []
for i in range(0,1):
    g = Game(P1=P1,P2=P2)
    wins_list.append(g.play())
learned_params = np.append(P1.eta_updates,P1.coeff)
np.savetxt('TD_coeff.txt',learned_params,delimiter=',')


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
function_names = function_names[1:]
weights = P1.coeff[1:]
plt.title("Player 1: Parameters")
plt.bar(function_names,weights)
plt.xticks(rotation='vertical')
plt.xlabel('Feature Scores')
plt.ylabel('Weight')

plt.figure(3)
function_names = []
for function in board.CBBFunc.getFunctionList():
    function_names.append(board.f.extractFunctionNameFromStrPointer(str(function)))
function_names = function_names[1:]
weights = P2.coeff[1:]
plt.title("Player 2: Parameters")
plt.bar(function_names,weights)
plt.xticks(rotation='vertical')
plt.xlabel('Feature Scores')
plt.ylabel('Weight')


plt.show()
np.set_printoptions(precision=None,linewidth=None)