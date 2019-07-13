import numpy as np
import board
updates = 0

for function in board.CBBFunc.getFunctionList():
    function_names = []
    print(board.f.extractFunctionNameFromStrPointer(str(function)))
    function_names.append(board.f.extractFunctionNameFromStrPointer(str(function)))
function_names = function_names[1:]
weights = P1.coeff[1:]
print(function_names)
print(weights)

for i in range(0,10):
    new_eta = np.random.randint(1,4)
    eta = 1/(updates+1)
    updates +=1
    print(eta)
    print(updates)
