import anytree as at
from math import inf

def ConstructAlphaBetaPrunedTree(state,ply=3,alpha=-inf,beta=+inf,thisNode=None,maximising=True,showAlphaBeta=True):
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
            if showAlphaBeta:
                child.ab = (alpha,beta)
            if alpha >= beta:
                break
    else: # minimising
        for transition in state.getTransitions():
            child = at.Node(str(transition),value=-inf)
            child.parent = thisNode
            next_state = state.advance(transition) 
            ConstructAlphaBetaPrunedTree(next_state,ply=ply-1,alpha=alpha,beta=beta,thisNode=child,maximising=True)
            thisNode.value = min(child.value,thisNode.value)
            beta = min(child.value,beta)
            if showAlphaBeta:
                child.ab = (alpha,beta)
            if alpha >= beta:
                break
    if thisNode == thisNode.root:
        return thisNode
    return None

def testFunction():
    from stateWithTrans import stateWithTrans
    S = stateWithTrans()
    X = ConstructAlphaBetaPrunedTree(S,ply=5)
    print(at.RenderTree(X))