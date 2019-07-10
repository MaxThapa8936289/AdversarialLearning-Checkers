import player as p

POS = p.b.MINIMAX_TEST2

def testAB():
    p1 = p.Player()
    A  = p.b.Board(pos=POS,show=True)
    X = p1.constructAlphaBetaPrunedCheckersTree(A)
    print(p.at.RenderTree(X))

def testMM():
    p2 = p.Player()
    B  = p.b.Board(pos=POS,show=False)
    Y = p2.calculateGameTree(B)
    Y = p.mnm.Minimax().minimax(Y)
    print(p.at.RenderTree(Y)) 

testAB()
testMM()