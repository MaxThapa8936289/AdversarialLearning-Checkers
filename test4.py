import anytree as at
import numpy as np

import minimax as mnm
import functions as f
import player as p
import board as b
import checkersBitBoardFunctions as CBBFunc
import time



A = b.Board(show=True)
P = p.Player()

t=time.time()
X = P._calculateGameTreeWithMaxMin2(A,ply=3)
#print("End Of Calculation")
#print(at.RenderTree(X))
T = time.time() - t
print("Minimax with AB Pruning took %f seconds" % T)

t=time.time()
X = P._calculateGameTreeWithMaxMin(A,ply=3)
#print("End Of Calculation")
#print(at.RenderTree(X))
T = time.time() - t
print("Minimax without AB Pruning took %f seconds" % T)