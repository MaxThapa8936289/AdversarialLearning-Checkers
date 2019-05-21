# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:52:44 2019

@author: MSGT
"""

import anytree as at

"""
Minimax algorithm prototype
Function: To search down the tree, find the minimax of each node, repeat up the 
tree.
Input: Input tree
Output: Input tree with modified values
Note: By default will maximise the first level, alternate going deeper
Note: Will be using anytree module for the tree functionality
Logistics:
    Step down the tree keeping track of wether to max or min
    evaluate terminal layer
    set score to layer above
    ??recursion??
    output result
"""


class Minimax:
    def __init__(self):
        return
        
    def minimax(self,gameTree,maxFirst=True,show=False):
        """ Function to recursively calculate the minimaxed value of an 
        anytree.Node object based on it's descendants. The leaves are expected 
        to have keyword argument "value" which is the parameter to be
        minimaxed.
        maxFirst=True by default, means the root node will be maximised across
        minimised children (and alternate each layer in the tree). 
        maxFirst = False will instead minimise across maximised children
        (and alternate each layer in the tree).
        """
        if type(gameTree) is not at.Node:
            raise TypeError("argument not an anytree.Node object")
        if show:
            print("Input Tree:")
            print(at.RenderTree(gameTree))
        if maxFirst:
            self._maximin(gameTree)
            if show:
                print("Minimaxed Tree:")
                print(at.RenderTree(gameTree))
            return gameTree
        else:
            self._minimax(gameTree)
            if show:
                print("Minimaxed Tree:")
                print(at.RenderTree(gameTree))
            return gameTree
    
    def _minimax(self,gameTree,show=False):
        """ Function to recursively calculate the minimaxed value of an 
        anytree.Node object based on it's descendants. The leaves are expected 
        to have keyword argument "value" which is the parameter to be
        minimaxed. The root node is MINIMISED.
        """
        for child in gameTree.children:
            if child.is_leaf:
                break
            else:
                self._maximin(child)
        values = [node.value for node in gameTree.children]
        gameTree.value = min(values)
        if show:
            print(values)
            print(gameTree.value)
        return
    
    def _maximin(self,gameTree,show=False):
        """ Function to recursively calculate the minimaxed value of an 
        anytree.Node object based on it's descendants. The leaves are expected 
        to have keyword argument "value" which is the parameter to be
        minimaxed. The root node is MAXIMISED.
        """
        for child in gameTree.children:
            if child.is_leaf:
                break
            else:
                self._minimax(child)
        values = [node.value for node in gameTree.children]
        gameTree.value = max(values)
        if show:
            print(values)
            print(gameTree.value)
        return
        
    def test(self):
        s0 = at.Node("s0",children=[at.Node("s00",value=1),at.Node("s01",value=2),at.Node("s02",value=3)],value=-1000)
        s1 = at.Node("s1",children=[at.Node("s10",value=4),at.Node("s11",value=5),at.Node("s12",value=6)],value=-1000)
        s2 = at.Node("s2",children=[at.Node("s20",value=7),at.Node("s21",value=8),at.Node("s22",value=9)],value=-1000)
        gameTree = at.Node("root",children=[s0,s1,s2],value=-1000)
        self.minimax(gameTree,show=True)
        return
    
    