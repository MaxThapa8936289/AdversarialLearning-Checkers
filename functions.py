# Misc functions and constants for Checkers Game 

# Binary positional constants
#   binary forms of the position arrays that are used for bitwise operations
#   only piece locations are represented
#   the colour will depend on context
import numpy as np
from re import search

# DEPRECIATED
#def diagonaliseBits(bit_int,length):
#    """ For use with bit representations of ints. Returns a list of int objects
#    where each element contains a single bit from the origonal int, all other
#    bits being zero. Where the bit string represents a boolean vector, this 
#    performs diagonalisation.
#    """
#    elements = [2**i for i in range(0,length)]
#    diagonal = [e & bit_int for e in elements]
#    return diagonal

def extractFunctionNameFromStrPointer(text):
    """ Extracts the function name from the output of str(function) 
    > text = str(some_function) 
    > print(text)
    >   '<function some_function at 0x0000000000000000>'
    > function_name = ExtractFunctionNameFromStrPointer(text)
    > print(function_name)
    >   'some_function'
    """
    try:
        found = search('<function (.+?) at', text).group(1)
    except AttributeError:
        # '<function ', ' at' not found in the original string
        found = '' # apply error handling
    return found
    
def revbits(x,size=32):
    """ Reverses the bits of an integer of size (default is 32) """
    return int(bin(x)[2:].zfill(size)[::-1], 2)

def binToBoolList(x):
    """ Converts binary int to list """
    return [int(d) for d in str(bin(x))[2:]]

def boolListToBin(lst):
    """ Converts a list of booleans to a binary int """
    return int(''.join(map(str, 1*lst)),2)

def printBin(x):
    print(bin(x)[2:].zfill(35))

# DEPRECIATED
#def randomPos2():
#    temp = randomPos()
#    am = boolPosToBin(temp==1)
#    ak = boolPosToBin(temp==2)
#    em = boolPosToBin(temp==-1)
#    ek = boolPosToBin(temp==-2)
#    return (am,ak,em,ek)
    
def range_of_man(sq, piece_colour):
    """ Return a nested dict of integer values corresponding to the movements 
    of a man of piece_colour on square sq
    """
    forward = piece_colour
    direction = {
        "right": {"slide": sq + (4*forward),
                  "jump": sq + (8*forward)},
        "left" : {"slide": sq + (5*forward), 
                  "jump": sq + (10*forward)}
    }
    return direction
            
def range_of_king(sq):
    direction = {
        "forward": { 
            "right": {"slide": sq+4, 
                      "jump": sq+8},
            "left" : {"slide": sq+5, 
                      "jump": sq+10}
            },
        "backward": {
            "right": {"slide": sq-4, 
                      "jump": sq-8},
            "left" : {"slide": sq-5, 
                      "jump": sq-10}
            }
    }
    return direction
