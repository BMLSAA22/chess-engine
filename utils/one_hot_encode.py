import numpy as np
def  hot_encode(piece):
    if piece.piece == "K" : a=[1,0,0,0,0,0]
    if piece.piece == "Q" : a=[0,1,0,0,0,0]
    if piece.piece == "R" : a=[0,0,1,0,0,0]
    if piece.piece == "B" : a=[0,0,0,1,0,0]
    if piece.piece == "N" : a=[0,0,0,0,1,0]
    if piece.piece == "P" : a=[0,0,0,0,1,0]


    if piece.color == "W" : a += [1]
    if piece.color == "B" : a += [0]


    if piece.moved : a = a + [1]
    else: a = a + [0]
    return np.array(a)
