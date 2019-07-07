import anytree as at
import numpy as np

import minimax as mnm
import functions as f
import player as p
import board as b
import checkersBitBoardFunctions as CBBFunc
import time

numIter = 100
mismatchCount = 0
Tmm = 0
Tab = 0
P = p.Player()

for i in range(0,numIter):
    A = b.Board(pos=CBBFunc.randomPos())
    
    t=time.time()
    X1 = P.makeMinimaxedMove(A)
    T1 = time.time() - t
    
    t=time.time()
    X2 = P.makeAlphaBetaMove(A)
    T2 = time.time() - t
    
    if np.array_equal(X1,X2):
        Tmm += T1
        Tab += T2
    else:
        mismatchCount += 1

tmm = Tmm/(numIter-mismatchCount)
tab = Tab/(numIter-mismatchCount)

print("Minimax without AB Pruning took on average %f seconds" % tmm)
print("Minimax with AB Pruning took %f seconds" % tab)
print("Algorithms failed to produce matching moves %f times" % mismatchCount)