# AdversarialLearning-Checkers

A program to simulate the game of English Checkers for the purpose of understanding machine learning in Python.

This is a WIP. Current functionality:
  - A 'board' class that represents the baord state. There are funcitons to change from one state to another via the rules of checkers.
  - A 'player' class that represents a mahine learning agent. Two options currently: 'random' chooses a random legal move each turn.
      'minimax' analyses all possible turns to a ply of 3, runs the minimax algorithm on the tresulting tree, chooses the minimaxed move.
      Node values are calculated via a constant weight vector and an feature vector for the state calculated via the board class. In             future the weight vector will be learned.
  - A 'game' class that can house two 'player' objects and will have them exchange 'board' states, thus simulating a game of checkers.
  - other files contain functions and are seperate for organisational purposes only. 
