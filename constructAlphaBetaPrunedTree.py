import anytree as at
from math import inf
from numpy import random

class state:
    def __init__(self,trans='a'):
        self.score = random.randint(0,50)
        self.transitions = ['a','b','c']
        
    def getTransitions(self):
        return self.transitions
        
    def advance(self,transition):
        if transition == 'a':
            new_state = state()
            return new_state
        if transition == 'b':
            new_state = state()
            return new_state
        if transition == 'c':
            new_state = state()
            return new_state

def ConstructAlphaBetaPrunedTree(state,ply=3,alpha=-inf,beta=+inf,thisNode=None,maximising=True):
    if thisNode == None: # at root
        thisNode = at.Node("root",value=-inf)
    if ply == 0:
        thisNode.value = state.score
        return None
    if maximising:
        for transition in state.getTransitions():
            child = at.Node(str(transition),value=+inf)
            child.parent = thisNode
            next_state = state.advance(transition) 
            ConstructAlphaBetaPrunedTree(next_state,ply=ply-1,alpha=alpha,beta=beta,thisNode=child,maximising=False)
            thisNode.value = max(child.value,thisNode.value)
            alpha = max(child.value,alpha)
            child.zab = (alpha,beta)
            if alpha >= beta:
                break
            #print(at.RenderTree(thisNode.root))
    else: # minimising
        for transition in state.getTransitions():
            child = at.Node(str(transition),value=-inf)
            child.parent = thisNode
            next_state = state.advance(transition) 
            ConstructAlphaBetaPrunedTree(next_state,ply=ply-1,alpha=alpha,beta=beta,thisNode=child,maximising=True)
            thisNode.value = min(child.value,thisNode.value)
            beta = min(child.value,beta)
            child.zab = (alpha,beta)
            if alpha >= beta:
                break
            #print(at.RenderTree(thisNode.root))
    if thisNode == thisNode.root:
        return thisNode
    return None

S = state()
X = ConstructAlphaBetaPrunedTree(S,ply=5)
print(at.RenderTree(X))