import numpy as np

###############################################################################
# BITBOARD CONSTANTS ##########################################################
###############################################################################
# Bit-board representations #
# Valid squares on the board
SQRS = 0b11111111011111111011111111011111111

# Rows
ROW1 = 0b00000000000000000000000000000001111
ROW2 = 0b00000000000000000000000000011110000
ROW3 = 0b00000000000000000000001111000000000
ROW4 = 0b00000000000000000011110000000000000
ROW5 = 0b00000000000001111000000000000000000
ROW6 = 0b00000000011110000000000000000000000
ROW7 = 0b00001111000000000000000000000000000
ROW8 = 0b11110000000000000000000000000000000

# Edges
EDGER= 0b00010000000010000000010000000010000
EDGEL= 0b00001000000001000000001000000001000

# 8 most central squares
CNTR = 0b00000000001100110001100110000000000

# Individual squares
SQ1 =  0b00000000000000000000000000000000001 
SQ2 =  0b00000000000000000000000000000000010
SQ3 =  0b00000000000000000000000000000000100
SQ4 =  0b00000000000000000000000000000001000
SQ5 =  0b00000000000000000000000000000010000
SQ6 =  0b00000000000000000000000000000100000
SQ7 =  0b00000000000000000000000000001000000
SQ8 =  0b00000000000000000000000000010000000
SQ9 =  0b00000000000000000000000001000000000
SQ10 = 0b00000000000000000000000010000000000
SQ11 = 0b00000000000000000000000100000000000
SQ12 = 0b00000000000000000000001000000000000
SQ13 = 0b00000000000000000000010000000000000
SQ14 = 0b00000000000000000000100000000000000
SQ15 = 0b00000000000000000001000000000000000
SQ16 = 0b00000000000000000010000000000000000
SQ17 = 0b00000000000000001000000000000000000
SQ18 = 0b00000000000000010000000000000000000
SQ19 = 0b00000000000000100000000000000000000
SQ20 = 0b00000000000001000000000000000000000
SQ21 = 0b00000000000010000000000000000000000
SQ22 = 0b00000000000100000000000000000000000
SQ23 = 0b00000000001000000000000000000000000
SQ24 = 0b00000000010000000000000000000000000
SQ25 = 0b00000001000000000000000000000000000
SQ26 = 0b00000010000000000000000000000000000
SQ27 = 0b00000100000000000000000000000000000
SQ28 = 0b00001000000000000000000000000000000
SQ29 = 0b00010000000000000000000000000000000
SQ30 = 0b00100000000000000000000000000000000
SQ31 = 0b01000000000000000000000000000000000
SQ32 = 0b10000000000000000000000000000000000

###############################################################################
# BIT MANIPULATION ############################################################
###############################################################################

def NOT35bit(x):
    """ Computes the logical compliment of a 35 bit binary number """
    return (0b11111111111111111111111111111111111 ^ x)

###############################################################################
# BIT TO LIST TRANSLATION #####################################################
###############################################################################

def binToBoolPos(x):
    """ Converts binary int to np.array of the same format as board.pos"""
    arr = [int(d) for d in str(bin(x))[2:]]
    len_dif = 35 - len(arr)
    if len_dif < 0:
        raise ValueError("Binary value too long for board")
    arr = np.array([0]*len_dif + arr)
    arr = np.delete(arr,[8,17,26])
    arr = arr.astype(int)
    return arr

def boolPosToBin(pos):
    """ Converts a board.pos boolean np.array to a binary number """
    pos = np.insert(pos,[8,16,24],False)
    return int(''.join(map(str, 1*pos)),2)

def boolPos2ToBin(pos):
    """ Converts a board.pos boolean np.array to a binary number """
    return int(''.join(map(str, 1*pos)),2)

def binToBoolPos2(x):
    """ Converts binary int to np.array of the same format as board.pos2"""
    arr = [int(d) for d in str(bin(x))[2:]]
    len_dif = 35 - len(arr)
    if len_dif < 0:
        raise ValueError("Binary value too long for board")
    arr = np.array([0]*len_dif + arr)
    arr = arr.astype(int)
    return arr

# DEPRECIATED
#def binToSqaures(x):
#    """ Converts 35bit int for use with the Board class to a list of tile 
#    numbers corresponding to the positions of the bits
#    """
#    arr = binToBoolPos(x)
#    arr = arr*SQUARES
#    arr = arr[arr!=0]
#    return arr
#
#def squaresToBin(tileList):
#    """ Converts a list of tile numbers to a 35bit int with '1' in the 
#    corresponding positions (for use with the Board class)
#    """
#    tmp = [0]*35
#    try:
#        # try as list (intended)
#        for tile in tileList:
#            tmp[-tile] = 1
#    except TypeError:
#        # try as scalar
#        tmp[-tileList] = 1
#    return int(''.join(map(str, 1*tmp)),2)

def randomPos():
    """ Returns a randomly generated position array """
    a = binToBoolPos2(np.random.randint(0,34359738367,dtype='int64')&SQRS)
    b = binToBoolPos2(np.random.randint(0,34359738367,dtype='int64')&SQRS)
    c = binToBoolPos2(np.random.randint(0,34359738367,dtype='int64')&SQRS)
    d = binToBoolPos2(np.random.randint(0,34359738367,dtype='int64')&SQRS)
    x = a+b # black pieces (overlap produces kings)
    y = c+d # red pieces (overlap produces kings)
    z = x - y # overall positions (overlap demotes pieces)
    # reduce density by 50%
    indices = np.random.choice(np.arange(z.size), replace=False,
                           size=int(z.size * 0.5))
    z[indices] = 0
    return z

###############################################################################
# ALLIED MOVES ################################################################
###############################################################################
def allied_RF_S(board):
    """ Returns the a bitboard integer corresponding to the tiles in which the 
    allied pieces can (S)lide to in a (R)ight (F)orward manner.
    """
    return (board.allies << 4) & board.empty

def allied_LF_S(board):
    """ Returns the a bitboard integer corresponding to the tiles in which the 
    allied pieces can (S)lide to in a (L)eft (F)orward manner.
    """
    return (board.allies << 5) & board.empty

def allied_RB_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (S)lide to in a (R)ight (B)ackward manner.
    """
    return (board.allied_kings >> 5) & board.empty

def allied_LB_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (S)lide to in a (L)eft (B)ackward manner.
    """
    return (board.allied_kings >> 4) & board.empty

def allied_RF_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (J)ump to in a (R)ight (F)orward manner.
    """
    return (board.allies << 8) & (board.enemies << 4) & board.empty

def allied_LF_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (J)ump to in a (L)eft (F)orward manner.
    """
    return (board.allies << 10) & (board.enemies << 5) & board.empty

def allied_RB_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (J)ump to in a (R)ight (B)ackward manner.
    """
    return (board.allied_kings >> 10) & (board.enemies >> 5) & board.empty

def allied_LB_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (J)ump to in a (L)eft (B)ackward manner.
    """
    return (board.allied_kings >> 8) & (board.enemies >> 4) & board.empty

def allied_Range_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (S)lide to.
    """
    _range = allied_RF_S(board) | allied_LF_S(board) \
        | allied_RB_S(board) | allied_LB_S(board)
    return _range

def allied_Range_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can (J)ump to.
    """
    _range = allied_RF_J(board) | allied_LF_J(board) \
        | allied_RB_J(board) | allied_LB_J(board)
    return _range

def allied_Range(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    allied pieces can legally move to.
    """
    ARJ = allied_Range_J(board)
    if ARJ:
        return ARJ
    else:
        return allied_Range_S(board)

###############################################################################
# ENEMY MOVES #################################################################
###############################################################################
def enemy_RF_S(board):
    """ Returns the a bitboard integer corresponding to the tiles in which the 
    enemy pieces can (S)lide to in a (R)ight (F)orward manner.
    """
    return (board.enemy_kings << 4) & board.empty

def enemy_LF_S(board):
    """ Returns the a bitboard integer corresponding to the tiles in which the 
    enemy pieces can (S)lide to in a (L)eft (F)orward manner.
    """
    return (board.enemy_kings << 5) & board.empty

def enemy_RB_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (S)lide to in a (R)ight (B)ackward manner.
    """
    return (board.enemies >> 5) & board.empty

def enemy_LB_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (S)lide to in a (L)eft (B)ackward manner.
    """
    return (board.enemies >> 4) & board.empty

def enemy_RF_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (J)ump to in a (R)ight (F)orward manner.
    """
    return (board.enemy_kings << 8) & (board.enemies << 4) & board.empty

def enemy_LF_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (J)ump to in a (L)eft (F)orward manner.
    """
    return (board.enemy_kings << 10) & (board.enemies << 5) & board.empty

def enemy_RB_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (J)ump to in a (R)ight (B)ackward manner.
    """
    return (board.enemies >> 10) & (board.enemies >> 5) & board.empty

def enemy_LB_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (J)ump to in a (L)eft (B)ackward manner.
    """
    return (board.enemies >> 8) & (board.enemies >> 4) & board.empty

def enemy_Range_S(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (S)lide to.
    """
    _range = enemy_RF_S(board) | enemy_LF_S(board) \
        | enemy_RB_S(board) | enemy_LB_S(board)
    return _range

def enemy_Range_J(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can (J)ump to.
    """
    _range = enemy_RF_J(board) | enemy_LF_J(board) \
        | enemy_RB_J(board) | enemy_LB_J(board)
    return _range

def enemy_Range(board):
    """ Returns the bitboard integer corresponding to the tiles in which the 
    enemy pieces can legally move to.
    """
    ARJ = enemy_Range_J(board)
    if ARJ:
        return ARJ
    else:
        return enemy_Range_S(board)
    
###############################################################################
# BOARD FEATURE ANALYSIS ######################################################
###############################################################################
    
def game_end_reward(board):
    reward_multiplier = 1000
    if allied_material_score(board) == 0:
        return -1*reward_multiplier # game lost
    elif enemy_material_score(board) == 0:
        return 1*reward_multiplier # game won
    else:
        return 0        

def getFunctionList():
    fnList = [allied_material_score, enemy_material_score,
              advancement_score, apex_score, 
              back_row_bridge_score, centre_control_1_score,
              centre_control_2_score, double_corner_score,
              cramp_score, deny_score]
    return fnList
    
def calculateFeatureScore(board,coeff):
    fnList = getFunctionList()
    if len(coeff) != len(fnList):
        raise ValueError("length of coeff must match number of functions in fnList")
    else:
        score = 0
        for i in range(len(fnList)):
            score += coeff[i]*fnList[i](board)
        return score

def showFeatureScore(board,coeff):
    fnList = getFunctionList()
    if len(coeff) != len(fnList):
        raise ValueError("length of coeff must match number of functions in fnList")
    else:
        score = []
        for i in range(len(fnList)):
            score.append(coeff[i]*fnList[i](board))
        return score     
    
def calculateFeatureVector(board,coeff):
    fnList = getFunctionList()
    if len(coeff) != len(fnList):
        raise ValueError("length of coeff must match number of functions in fnList")
    else:
        featureVector = []
        for i in range(len(fnList)):
            featureVector.append(fnList[i](board))
        return np.array(featureVector)
    
def allied_material_score(board):
    return bin(board.allies).count('1')

def enemy_material_score(board):
    return bin(board.enemies).count('1')

def advancement_score(board):
    credit = bin(board.enemies & (ROW3 | ROW4)).count('1')
    debit = bin(board.enemies & (ROW5 | ROW6)).count('1')
    return (credit - debit)

def apex_score(board):
    if(board.allied_kings | board.enemy_kings):
        return 0
    else:
        en = bool(SQ7 & NOT35bit(board.enemy_men))  \
            and bool(SQ26 & NOT35bit(board.enemy_men))
        al = bool(board.allied_men & (SQ7 | SQ26))
        debit = int(en and al)
        return - debit

def back_row_bridge_score(board):
    if(board.allied_kings | board.enemy_kings):
        return 0
    else:
        bck = bool(SQ30 & board.enemy_men) and bool(SQ32 & board.enemy_men)
        credit = int(bck)
        return credit
    
def centre_control_1_score(board):
    credit = bin(board.enemy_men & CNTR).count('1')
    return credit

def centre_control_2_score(board, allied_range=None):
    if allied_range is not None:
        credit = bin(board.allies & CNTR).count('1')
        credit += bin(allied_range & CNTR).count('1')
        return credit
    else:
        AR = allied_Range(board)
        return centre_control_2_score(board, allied_range=AR)
   
def double_corner_score(board, allied_range=None):
    if allied_range is not None:
        credit = 0
        al = allied_material_score(board)
        if (al < 7):
            if (al < enemy_material_score(board)):
                if ( allied_range & (SQ1 | SQ5 | SQ28 | SQ32)):
                    credit = 1
        return credit
    else:
        AR = allied_Range(board)
        return double_corner_score(board, allied_range=AR)


def cramp_score(board):
    credit = 0
    if ((board.enemies & SQ20) and (board.enemies & (SQ19 | SQ24))):
        if ((board.enemies & SQ8) 
            and (board.enemies & SQ11)
            and (board.enemies & SQ12)
            and (board.enemies & SQ16)
        ):
            credit = 2
    return credit

def deny_score(board,show_details=False):
    """Function to determine the denial of occupancy of each square on the 
    board and sum the total. Denial of occupancy of a square is 1 if an
    active piece can move into it and the passive side can capture it 
    without an exchange, and is 0 otherwise.
    
    Four digonal move directions are consideren independantly. All moves in
    each direction are considered simultaneously for the purpose of
    locating the squares in which the active sides moves may be captured.
    (This is achieved by combing the move squares with the origonal empties 
    and the enemy locations. Using the origonal empties prevents false 
    empties arising by nature of the parallel calculation. However, a 
    conditional workaround is necessary for the case of a capture in the 
    opposite direction to the move.)
    
    The origonal piece locations are used to determine the presence of a 
    possible exchnge. 4 directions of capture each have 3 possible 
    exchanges. ALL exchanges of the 3 must be impossible for the direction 
    of capture to deny occupancy. If ANY direction of 
    capture results in denied occupancy, the square is denied occupancy and
    contributes 1 to the score.
    
    """
    
    credit = 0
    capturable_RF_moves = \
    allied_RF_S(board) & NOT35bit(EDGER | ROW8) & SQRS
    capturable_LF_moves = \
    allied_LF_S(board) & NOT35bit(EDGEL | ROW8) & SQRS
    capturable_RB_moves = \
    allied_RB_S(board) & NOT35bit(EDGER | ROW1) & SQRS
    capturable_LB_moves = \
    allied_LB_S(board) & NOT35bit(EDGEL | ROW1) & SQRS
    capturable_moves_list = [capturable_RF_moves,capturable_LF_moves,
                             capturable_RB_moves,capturable_LB_moves]
    for i in range(len(capturable_moves_list)):
        moves = capturable_moves_list[i]
        LBC, LBC_RFE, LBC_LFE, LBC_RBE = 0, 0, 0, 0
        RBC, RBC_LFE, RBC_RFE, RBC_LBE = 0, 0, 0, 0
        LFC, LFC_RBE, LFC_LBE, LFC_RFE = 0, 0, 0, 0
        RFC, RFC_LBE, RFC_RBE, RFC_LFE = 0, 0, 0, 0
        # LBC = Left Backward Capture, RFE = Right Forward Exchange, etc.
        LBC = moves & (board.enemies >> 4) & (board.empty << 4)
        # Note: If i = 0, the move is RF and an empty space behind the move
        # is certain, so LBC is guaranteed. However, it will not evaulate 
        # as such because board.empty does not include the square from which
        # the move was made. Therfore, on the condition of an RF move, we 
        # assume the empty space. Unfortunately, this does make the 
        # ordering of capturable_moves_list important.
        # Similarly, if the move is RF, then RFC is impossible. We use this
        # to save a few calcualtions
        if(i==0): LBC = moves & (board.enemies >> 4)
        if(i!=3):
            LBC_RFE = LBC & NOT35bit(board.allies << 8)
            LBC_LFE = LBC & NOT35bit((board.allies << 9) & (board.empty >> 1))
            LBC_RBE = LBC & NOT35bit((board.allied_kings >> 1) & (board.empty << 9)) 
        # RBC = Right Backward Capture, etc.
        RBC = moves & (board.enemies >> 5) & (board.empty << 5)
        if(i==1): RBC = moves & (board.enemies >> 5)
        if(i!=2):
            RBC_LFE = RBC & NOT35bit(board.allies << 10)
            RBC_RFE = RBC & NOT35bit((board.allies << 9) & (board.empty << 1)) 
            RBC_LBE = RBC & NOT35bit((board.allied_kings << 1) & (board.empty << 9)) 
        # LFC = Left Forward Capture, etc.
        LFC = moves & (board.enemy_kings << 5) & (board.empty >> 5)
        if(i==2): LFC = moves & (board.enemy_kings << 5)
        if(i!=1):
            LFC_RBE = LFC & NOT35bit(board.allied_kings >> 10)
            LFC_LBE = LFC & NOT35bit((board.allied_kings >> 9) & (board.empty >> 1))
            LFC_RFE = LFC & NOT35bit((board.allies >> 1) & (board.empty >> 9))
        # RFC = Left Forward Capture, etc.
        RFC = moves & (board.enemy_kings << 4) & (board.empty >> 4)
        if(i==3): RFC = moves & (board.enemy_kings << 4)
        if(i!=0):
            RFC_LBE = RFC & NOT35bit(board.allied_kings >> 8)
            RFC_RBE = RFC & NOT35bit((board.allied_kings >> 9) & (board.empty << 1)) 
            RFC_LFE = RFC & NOT35bit((board.allies << 1) & (board.empty >> 9)) 
        denial =  (LBC_RFE & LBC_LFE & LBC_RBE) \
                | (RBC_LFE & RBC_RFE & RBC_LBE) \
                | (LFC_RBE & LFC_LBE & LFC_RFE) \
                | (RFC_LBE & RFC_RBE & RFC_LFE)
        if show_details:
            foo = [[LBC_RFE,LBC_LFE,LBC_RBE],
                   [RBC_LFE,RBC_RFE,RBC_LBE],
                   [LFC_RBE,LFC_LBE,LFC_RFE],
                   [RFC_LBE,RFC_RBE,RFC_LFE]]
            bar = np.transpose(np.array([[bin(i) for i in j] for j in foo]))
            print("i = %d" % i)
            print(foo)
            print(bar)
        credit += bin(denial).count('1')
    return credit
