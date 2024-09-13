piece={
     'p':0,
     'k':1,
     'q':2,
     'r':3,
     'b':4,
     'n':5
}
import numpy as np
def decode_FEN(pos):
    # Split the FEN string into its components
    game=pos.split(' ')[0]
    info=pos.split(' ')[1:]
    rows = game.split("/")
    # Check if there are enough fields (10) in the FEN string
    rows=[list(i) for i in rows]
    board=[]
    for row in rows:

            s=[]
            for sq in row:
                if ord(sq)>48 and ord(sq)<57:
                    s=s+['']*int(sq)
                else:s.append(sq)
            board.append(s)
    return board , info 


def decode_extra_info (f):
    arr=np.zeros(5)
    if f[0]=='w':arr[0]=1
    if 'K' in f[1]:arr[1]=1
    if 'Q' in f[1]:arr[2]=1
    if 'k' in f[1]:arr[3]=1
    if 'Q' in f[1]:arr[4]=1
    return arr
     
     
        
        


def FEN_to_arr(game):
    arr,info=decode_FEN(game)
    tensor=np.zeros((6,8,8))
    for i in range(8):
        for j in range(8):
            if arr[i][j]!='':
                if arr[i][j].islower():tensor[piece[arr[i][j]]][i][j]=-1
                else:tensor[piece[arr[i][j].lower()]][i][j]=1
    return tensor , decode_extra_info(info)
print(FEN_to_arr("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"))

