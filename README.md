# AdversarialLearning-Checkers

A program to simulate the game of English Checkers for the purpose of understanding machine learning in Python.

board.py - contains a class and related functions to capture the state of the game during any one turn. Also conains a function to change from one state to another, i.e make a move.

player.py - contains a class and related functions to allow an agent to operate on the game. The player class can be instantiated as a number of agent types, including random, TD-Learning, and human.

game.py - contains a class to host an ongoing game. Each instance msut have two agents (the players) and the class facilitates the passing of board states between the players to simulate play. 
	Currently, the game.py file also contains the data generation code, and some quick graphing.

functions.py - various associated functions for the operation of the program.

checkersBitBoardFunctions.py - various functions required to make calculations and evaluations on the board BitBoard represenation.

changelog.txt - Log of changes and updates to the project. 
