import board as b
import numpy as np
import time
import anytree as at
import minimax as mnm
from math import inf

# Player Class for Checkers game
#   A class to emulate a player in the game of checkers. This class will
#   perform the analysis ond learning of the game.
# Plan:
#   Create randomly playing player first
#   Pitch two random players against one another
#   Impliment a win system
# Player Class
# Properties:   Saved Boards, analysis of future moves, 
#
# Initialisers: playstyle
#

COEFF = [100,-100,0,0,0,3,2,0,0,10]

class Player:
    def __init__(self,agent="random",name=None,delay=0):
        self.name = name
        self.delay = delay
        self.agent = agent
        
    def getName(self):
        return self.name
    
    def makeMove(self,board):
        if self.agent == "random":
            return self.makeRandomMove(board)
        elif self.agent == "minimax":
            return self.makeMinimaxedMove(board)
        elif self.agent == "alphaBeta":
            return self.makeAlphaBetaMove(board)
        else:
            raise ValueError("argument does not match a possible agent type: \
                             'random' or 'minimax' or 'alphaBeta'")
    
    def chooseMove(self,board):
        # Calculate game tree of boarde
        gameTree = self.calculateGameTree(board,coeff=COEFF,ply=3)
        # minimax tree
        minmax_gameTree = mnm.Minimax().minimax(gameTree)
        # search for matching nodes from children 
        # level 1 = root, level 2 = children. (may be multiple nodes)
        best_move_nodes = at.search.findall_by_attr(minmax_gameTree,
                                                 minmax_gameTree.value,
                                                 name="value",maxlevel=2)
        # select random move from equally best scoring ones
        randindex = np.random.randint(1,len(best_move_nodes)) # 0th item is always root
        move = best_move_nodes[randindex].move
        return move
    
    def calculateGameTree(self,board,coeff=COEFF,ply=3,parent=None):
        if parent is None:
            gameTree = at.Node("root",value=-inf)
        for move in board.getAvailableMoves():
            if parent is None:
                node = at.Node(str(move),parent=gameTree,move=move,value=-inf)
            else:
                node = at.Node(str(move),parent=parent,move=move,value=-inf)
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                self.calculateGameTree(next_board,coeff,ply=ply-1,parent=node)
            else:
                score = next_board.feature_score(coeff)
                node.value = score
                #node.scores = b.CBBFunc.showFeatureScore(next_board,coeff)
        if parent is None:
            return gameTree

    def constructAlphaBetaPrunedCheckersTree(self,board,coeff=COEFF,depth=2,alpha=-inf,beta=+inf,thisNode=None,maximising=True,showAlphaBeta=True):
        if thisNode == None: # at root
            thisNode = at.Node("root")
        if depth == 0:
            thisNode.value = board.feature_score(coeff)
            #thisNode.scores = b.CBBFunc.showFeatureScore(board,coeff)
            return None
        if maximising:
            thisNode.value = -inf
            for move in board.getAvailableMoves():
                child = at.Node('b'+str(move))
                child.move = move
                child.parent = thisNode
                next_state = b.move(board,move,show=False) 
                if next_state.turn != board.turn: # minimise oponent
                    self.constructAlphaBetaPrunedCheckersTree(next_state,depth=depth,alpha=alpha,beta=beta,thisNode=child,maximising=False)
                else:   # maximise self
                    self.constructAlphaBetaPrunedCheckersTree(next_state,depth=depth,alpha=alpha,beta=beta,thisNode=child,maximising=True)
                thisNode.value = max(child.value,thisNode.value)
                alpha = max(child.value,alpha)
                if showAlphaBeta:
                    thisNode.ab = (alpha,beta)
                if alpha >= beta:
                    break
        else: # minimising
            thisNode.value = +inf
            for move in board.getAvailableMoves():
                child = at.Node('r'+str(move))
                child.move = move
                child.parent = thisNode
                next_state = b.move(board,move,show=False) 
                if next_state.turn != board.turn: # maximise self
                    self.constructAlphaBetaPrunedCheckersTree(next_state,depth=depth-1,alpha=alpha,beta=beta,thisNode=child,maximising=True)
                else:   # minimise oponent
                    self.constructAlphaBetaPrunedCheckersTree(next_state,depth=depth,alpha=alpha,beta=beta,thisNode=child,maximising=False)
                thisNode.value = min(child.value,thisNode.value)
                beta = min(child.value,beta)
                if showAlphaBeta:
                    thisNode.ab = (alpha,beta)
                if alpha >= beta:
                    break
        if thisNode == thisNode.root:
            return thisNode
        return None

    def makeRandomMove(self,board):
        availableMoves = board.getAvailableMoves()
        time.sleep(self.delay)
        move_index = np.random.randint(0,len(availableMoves))
        #print("making random move")
        return b.move(board,availableMoves[move_index])
    
    def makeMinimaxedMove(self,board):
        move = self.chooseMove(board)
        time.sleep(self.delay)
        #print("making minimaxed move")
        return b.move(board,move)
    
    def makeAlphaBetaMove(self,board):
        movetree = self.constructAlphaBetaPrunedCheckersTree(board)
        # level 1 = root, level 2 = children. (may be multiple nodes)
        best_move_nodes = at.search.findall_by_attr(movetree,
                                                 movetree.value,
                                                 name="value",maxlevel=2)
        # select random move from equally best scoring ones
        randindex = np.random.randint(1,len(best_move_nodes)) # 0th item is always root
        move = best_move_nodes[randindex].move
        return b.move(board,move)
        
        

        
    