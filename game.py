import board as board
import player
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
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
TURNS = 1000


class Game:
    def __init__(self,P1=player.Player(delay=DELAY,agent="alphaBeta"),P2=player.Player(delay=DELAY,agent="alphaBeta"),start_pos=board.START_POS):
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
                            
            if counter == TURNS: # draw
                finished = True
                winner = "DRAW"
                print("DRAW")
                print("Game length: %r turns over %.5f seconds" % (counter, (time.time() - start_time)))
                
            elif new_board.availableMoves.size == 0: # game won
                
                # Allow losing player learn if it can
                if new_board.turn == board.BLACK:
                    losing_player = self.P1
                elif new_board.turn == board.RED:
                    losing_player = self.P2
                if losing_player.agent == "TDLearning":
                    losing_player.updateWeightsWithTDLearning(new_board)
                
                # end game    
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
coefficient_history = []
eta_history = []
for i in range(0,1):
    print("\n")
    print("GAME ", i+1)
    print("\n")
    g = Game(P1=P1,P2=P2)
    wins_list.append(g.play())
    coefficient_history.append(copy(P1.coeff))
    eta_history.append(P1.eta)
coefficient_history = np.array(coefficient_history)
eta_history = np.array(eta_history)
np_wins_list = np.array(wins_list)
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

plt.figure(4)
cum_black_wins = np.cumsum(np_wins_list == "BLACK")
cum_red_wins = np.cumsum(np_wins_list == "RED")
cum_draws = np.cumsum(np_wins_list == "DRAW")
games = [i+1 for i in range(0,len(wins_list))]
plt.title("Plot of wins over time")
plt.plot( games, cum_black_wins, marker='o', markerfacecolor='k', markersize=4, color='k', linewidth=1)
plt.plot( games, cum_red_wins, marker='o', markerfacecolor='r', markersize=4, color='r', linewidth=1)
plt.plot( games, cum_draws, marker='o', markerfacecolor='grey', markersize=4, color='grey', linewidth=1)
plt.xlabel('Games finished')
plt.ylabel('Cumulative Wins')

fig = plt.figure(5)
ax = fig.add_subplot(111)
plt.title("Feature Weights after each game")
plt.xlabel('Games finished')
plt.ylabel('Coffecient Value')

Set1 = cm = plt.get_cmap('Set1') 
cNorm  = colors.Normalize(vmin=0, vmax=9)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=Set1)

lines = []
for idx in range(10):
    colorVal = scalarMap.to_rgba(idx)
    line, = ax.plot(games,
                       coefficient_history[:,idx],
                       marker='o',
                       markerfacecolor=colorVal,
                       markersize = 2,
                       linewidth = 1,
                       color=colorVal,
                       label=function_names[idx])
    lines.append(line)
for i in range(0,len(wins_list)):
    if wins_list[i] == "BLACK":
        ax.axvspan(i+0.1, i+1.1, facecolor='g', alpha=0.2)
    elif wins_list[i] == "RED":
        ax.axvspan(i+0.1, i+1.1, facecolor='r', alpha=0.2)
    else:
        ax.axvspan(i+0.1, i+1.1, facecolor='grey', alpha=0.2)    
handles,labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper right')
ax.grid()


plt.figure(6)
plt.title("Eta Value after each game")
plt.plot( games, eta_history, marker='o', markerfacecolor='k', markersize=2, color='k', linewidth=1)
for i in range(0,len(wins_list)):
    if wins_list[i] == "BLACK":
        plt.axvspan(i+0.1, i+1.1, facecolor='g', alpha=0.2)
    elif wins_list[i] == "RED":
        plt.axvspan(i+0.1, i+1.1, facecolor='r', alpha=0.2)
    else:
        plt.axvspan(i+0.1, i+1.1, facecolor='grey', alpha=0.2)    
plt.xlabel('Games finished')
plt.ylabel('Coffecient Value')

plt.show()
np.set_printoptions(precision=None,linewidth=None)