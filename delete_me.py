import board as b
import player as p
import numpy as np

A = np.array([[2,3],[10,21],[30,33]])
B = np.array([[11,17]])
C = np.array([11,19])
D = [10,21]
E = [[10,21],[22,30]]

tests = [A,B,C,D,E]
squares = []

for t in tests:
    print(t)
    
print("\n")    

for example in tests:
    squareExample = b.f.posMovesToSquaresMoves(example)
    squares.append(squareExample)
    print(squareExample)

print("\n")

for example in squares:
    posExample = b.f.squaresMovesToPosMoves(example)
    print(posExample)
    
