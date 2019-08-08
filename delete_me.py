import board as b
import numpy as np

A = b.Board()
A.display()
B = b.move(A,b.f.readMovesToPosMoves([11,15]))
A = b.move(B,b.f.readMovesToPosMoves([23,18]))
B = b.move(A,b.f.readMovesToPosMoves([7,11]))
A = b.move(B,b.f.readMovesToPosMoves([21,17]))
B = b.move(A,b.f.readMovesToPosMoves([10,14]))
A = b.move(B,b.f.readMovesToPosMoves([17,10]))
print(b.f.posMovesToReadMoves(A.availableMoves))
    


