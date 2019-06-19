import board as b
import numpy as np
import time
import anytree as at
import minimax as mnm
import math

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

COEFF = [200,-100,0,0,0,3,2,0,0,10]

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
        else:
            raise ValueError("argument does not match a possible agent type: \
                             'random' or 'minimax'")
    
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
            gameTree = at.Node("root",value=-math.inf)
        for move in board.getAvailableMoves():
            if parent is None:
                node = at.Node(str(move),parent=gameTree,move=move,value=-math.inf)
            else:
                node = at.Node(str(move),parent=parent,move=move,value=-math.inf)
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                self.calculateGameTree(next_board,coeff,ply=ply-1,parent=node)
            else:
                score = next_board.feature_score(coeff)
                node.value = score
        if parent is None:
            return gameTree
        
    def calculateGameTreeWithMiniMax(self,board,coeff=COEFF,ply=3,parent=None):
        return self._calculateGameTreeWithMaxMin(board=board,coeff=coeff,ply=ply,parent=parent)
    
    def _calculateGameTreeWithMaxMin(self,board,coeff=COEFF,ply=3,parent=None):
        if parent is None:
            gameTree = at.Node("root",value=-math.inf)
            parent = gameTree
        for move in board.getAvailableMoves():
            node = at.Node(str(move),parent=parent,move=move,value=-math.inf)
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                self._calculateGameTreeWithMinMax(next_board,coeff,ply=ply-1,parent=node)
            else:
                score = next_board.feature_score(coeff)
                node.value = score
        values = [node.value for node in parent.children]
        parent.value = max(values)
        if parent.name == "root":
            return gameTree
    
    def _calculateGameTreeWithMinMax(self,board,coeff=COEFF,ply=3,parent=None):
        if parent is None:
            gameTree = at.Node("root",value=-math.inf)
            parent = gameTree
        for move in board.getAvailableMoves():
            node = at.Node(str(move),parent=parent,move=move,value=-math.inf)
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                self._calculateGameTreeWithMaxMin(next_board,coeff,ply=ply-1,parent=node)
            else:
                score = next_board.feature_score(coeff)
                node.value = score
        values = [node.value for node in parent.children]
        parent.value = min(values)
        if parent.name == "root":
            return gameTree

    def calculateGameTreeWithMiniMax2(self,board,coeff=COEFF,ply=3,parent=None):
        return self._calculateGameTreeWithMaxMin2(board=board,coeff=coeff,ply=ply,parent=parent)
    
    def _calculateGameTreeWithMaxMin2(self,board,coeff=COEFF,ply=3,atRoot=True,thisNode=None,gameTree=None):
        if atRoot:
            gameTree = at.Node("root",value=-math.inf)
            thisNode = gameTree
        for move in board.getAvailableMoves():
            child = at.Node(str(move),move=move,value=+math.inf)
            child.parent = thisNode
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                try:
                    self._calculateGameTreeWithMinMax2(next_board,coeff,ply=ply-1,atRoot=False,thisNode=child,gameTree=gameTree)
                except(ValueError):
                    break
                except:
                    raise RuntimeError("_calculateGameTreeWithMinMax2 experienced an error in execution")
            else:
                score = next_board.feature_score(coeff)
                child.value = score
                if score > thisNode.parent.value:
                    thisNode.value = score
                    break
                if score > thisNode.value:
                    thisNode.value = score
                #print(at.RenderTree(gameTree))
        if atRoot:
            return gameTree
        elif thisNode.parent.name != "root" and thisNode.value < thisNode.parent.parent.value:
            thisNode.parent.value = thisNode.value
            raise ValueError
        elif thisNode.value < thisNode.parent.value:
            thisNode.parent.value = thisNode.value
        #print(at.RenderTree(gameTree))
        return None
            
    
    def _calculateGameTreeWithMinMax2(self,board,coeff=COEFF,ply=3,atRoot=True,thisNode=None,gameTree=None):
        if atRoot:
            gameTree = at.Node("root",value=+math.inf)
            thisNode = gameTree
        for move in board.getAvailableMoves():
            child = at.Node(str(move),move=move,value=-math.inf)
            child.parent = thisNode
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                try:
                    self._calculateGameTreeWithMaxMin2(next_board,coeff,ply=ply-1,atRoot=False,thisNode=child,gameTree=gameTree)
                except(ValueError):
                    break
                except:
                    raise RuntimeError("_calculateGameTreeWithMaxMin2 experienced an error in execution")
            else:
                score = next_board.feature_score(coeff)
                child.value = score
                if score < thisNode.parent.value:
                    thisNode.value = score
                    break
                if score < thisNode.value:
                    thisNode.value = score
                #print(at.RenderTree(gameTree))
        if atRoot:
            return gameTree
        elif thisNode.parent.name != "root" and thisNode.value > thisNode.parent.parent.value:
            thisNode.parent.value = thisNode.value
            raise ValueError
        elif thisNode.value > thisNode.parent.value:
            thisNode.parent.value = thisNode.value
        #print(at.RenderTree(gameTree))
        return None
        
    
    def makeMinimaxedMove(self,board):
        move = self.chooseMove(board)
        time.sleep(self.delay)
        #print("making minimaxed move")
        return b.move(board,move)
    
    def makeRandomMove(self,board):
        availableMoves = board.getAvailableMoves()
        time.sleep(self.delay)
        move_index = np.random.randint(0,len(availableMoves))
        #print("making random move")
        return b.move(board,availableMoves[move_index])
        
    