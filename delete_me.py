import board as b
import numpy as np

total_blacks = 0
total_reds = 0
iters = 100
for i in range(0,iters):
    A = b.Board(pos=b.CBBFunc.randomPos())
    total_blacks += b.CBBFunc.allied_material_score(A)
    total_reds += b.CBBFunc.enemy_material_score(A)

print("Ratio of black to red is %f" % (total_blacks/total_reds))


    


