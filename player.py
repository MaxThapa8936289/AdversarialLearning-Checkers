import board as b
import numpy as np
import time
import anytree as at
import minimax as mnm
from math import inf
from re import search

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
        
        if self.agent in ["random","minimax","alphaBeta","human"]:
            self.coeff = COEFF
        elif self.agent == "TDLearning":
            try:
                self.learned_params = np.loadtxt('TD_coeff.txt')
            except IOError:
                print("No file named 'TD_coeff.txt' found")
                print("Initialising new learning parameters...")
                self.learned_params = [1,0,0,0,0,0,0,0,0,0,0]
                
            self.eta_updates = self.learned_params[0]
            self.coeff = self.learned_params[1:]
            self.eta = 1/self.eta_updates
        else:
            raise ValueError("argument does not match a possible agent type: \
                             'random' or 'minimax' or 'alphaBeta' 'human' or 'TDLearning'")
            
    def getName(self):
        return self.name
    
    def makeMove(self,board):
        if self.agent == "random":
            return self.makeRandomMove(board)
        elif self.agent == "minimax":
            return self.makeMinimaxedMove(board)
        elif self.agent == "alphaBeta":
            return self.makeAlphaBetaMove(board)
        elif self.agent == "human":
            return self.makeHumanMove(board)
        elif self.agent == "TDLearning":
            return self.makeAlphaBetaMove(board)
        else:
            raise ValueError("argument does not match a possible agent type: \
                             'random' or 'minimax' or 'alphaBeta' or 'TDLearning'")
        
    def calculateGameTree(self,board,ply=3,parent=None):
        if parent is None:
            gameTree = at.Node("root",value=-inf)
        for move in board.getAvailableMoves():
            if parent is None:
                node = at.Node(str(move),parent=gameTree,move=move,value=-inf)
            else:
                node = at.Node(str(move),parent=parent,move=move,value=-inf)
            next_board = b.move(board,move,show=False) 
            if ply != 1:
                self.calculateGameTree(next_board,ply=ply-1,parent=node)
            else:
                score = next_board.feature_score(self.coeff)
                node.value = score
                #node.scores = b.CBBFunc.showFeatureScore(next_board,self.coeff)
        if parent is None:
            return gameTree

    def constructAlphaBetaPrunedCheckersTree(self,board,depth=2,alpha=-inf,beta=+inf,thisNode=None,maximising=True,showAlphaBeta=True):
        if thisNode == None: # at root
            thisNode = at.Node("root")
        if depth == 0:
            thisNode.value = board.feature_score(self.coeff)
            #thisNode.scores = b.CBBFunc.showFeatureScore(board,self.coeff)
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
        # Calculate game tree of boarde
        gameTree = self.calculateGameTree(board,ply=3)
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
        time.sleep(self.delay)
        return b.move(board,move)

    def makeAlphaBetaMove(self,board):
        # start tracking passed time
        t = time.time()
        # Construct the tree of moves to consider
        movetree = self.constructAlphaBetaPrunedCheckersTree(board)
        # extract best move
        # level 1 = root, level 2 = children. (may be multiple nodes)
        best_move_nodes = at.search.findall_by_attr(movetree,
                                                 movetree.value,
                                                 name="value",maxlevel=2)
        # select random move from equally best scoring ones
        randindex = np.random.randint(1,len(best_move_nodes)) # 0th item is always root
        move = best_move_nodes[randindex].move
        # print move choice for human player to read
        printMove = b.f.posMovesToReadMoves(move)
        print("%s makes move: %d to %d" % (b.turn_to_string(board.turn),printMove[0],printMove[1]))
        # slow down turn
        sleepTime = self.delay - (time.time() - t)
        if sleepTime > 0:
            time.sleep(sleepTime)
        return b.move(board,move)
    
    def updateWeightsWithTDLearning(self,previousState,currentState):
        prediction = previousState.feature_score(self.coeff)
        reward = b.CBBFunc.game_end_reward(currentState)
        targetScore = currentState.feature_score(self.coeff)
        target = reward + targetScore
        p_minus_t = prediction - target
        gradient = b.CBBFunc.calculateFeatureVector(previousState,self.coeff)
#        # print result for debugging
#        print("prediction: ", prediction)
#        print("target: " , reward, " + ", targetScore)
#        print("weights: ", self.coeff)
#        print("gradient/feature vector: ", gradient)
#        print("update increment: ", self.eta*p_minus_t*gradient )
        # TD-Learning update
        new_coeff = self.coeff - self.eta*p_minus_t*gradient
        if(not np.array_equal(new_coeff,self.coeff)): # non-trivial update
            # Update Eta
#            print("updating eta!")
            self.eta_updates += 1
            self.eta = 1/(self.eta_updates)
            self.coeff = new_coeff
#        print(self.coeff)
    
    def makeHumanMove(self,board):
        print("The available moves for this turn are:")
        availableMoves = b.f.posMovesToReadMoves(board.getAvailableMoves())
        for item in availableMoves:
            print(item[0], " to ", item[1])
        validMove = False
        while validMove is False:
            moveStr = input("Please select a move by entering a pair of numbers 'xx yy', representing the move from square xx to yy: ")
            move = np.array([[0,0]])
            try:
                if moveStr == "exit":
                    raise SystemExit("Requested 'exit'. Ending program...")
                if len(moveStr) < 3:
                    raise ValueError('Insufficient length')
                move0 = search(r'^([0-9]|[0-9][0-9])\b',moveStr).group(1)
                move1 = search(r'\b([0-9]|[0-9][0-9])$',moveStr).group(1)
                move[0][0] = int(move0)
                move[0][1] = int(move1)

                if move[0].tolist() not in availableMoves.tolist():
                    raise ValueError('Illegal move')
                
                print("Move Accepted")
                move = b.f.readMovesToPosMoves(move)
                print(move)
                validMove = True
                
            except AttributeError:
                print("Sorry, the move was not valid. Please check for typos and try again...")
            except ValueError as ValErr:
                arg = ValErr.args
                if arg[0] == 'Insufficient length':
                    print("Sorry, the move entered was not valid. Please enter a pair of numbers.")
                if arg[0] == 'Illegal move':
                    print("Sorry but that move is not legal. Please choose from the list of available moves this turn:")
                    for item in availableMoves:
                        print(item[0], " to ", item[1])
        return b.move(board,move[0])
                
                
    
        
        
    
        
        

        
    