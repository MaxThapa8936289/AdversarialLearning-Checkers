from numpy import random
class stateWithTrans:
    def __init__(self,trans='a'):
        self.score = random.randint(0,50)
        self.transitions = ['a','b','c']
        
    def getTransitions(self):
        return self.transitions
        
    def advance(self,transition):
        if transition == 'a':
            new_state = stateWithTrans()
            return new_state
        if transition == 'b':
            new_state = stateWithTrans()
            return new_state
        if transition == 'c':
            new_state = stateWithTrans()
            return new_state