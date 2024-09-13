def abs(num):
    if num < 0:
        return -num
    return num
def diagonal(piece,board):
    pos=piece.position
    moves=[]
    for i in [-1,1]:
        for j in [-1,1]:
            for k in range(1,8):
                
                if (pos[0] + ( i * k ) <=8 and pos[0] + ( i * k ) > 0 and pos[1] + ( j * k ) <=8 and pos[1] + ( j * k ) > 0 ):
                    
                    if board[(pos[0]+i*k,pos[1]+j*k)]=="":  
                        moves.append((pos[0]+i*k,pos[1]+j*k))
                        
                    elif board[(pos[0]+i*k,pos[1]+j*k)].color != piece.color:
                        moves.append((pos[0]+i*k,pos[1]+j*k))
                        break
                    else:break
                        
                    
    return moves

def rook(piece,board):
    pos=piece.position
   
    moves=[]
    for i in [-1,1]: 
            a=True       
            for k in range(1,8):
                
                if (pos[0]+(i*k) <=8 and pos[0]+(i*k) > 0 and a):
                    if board[(pos[0]+i*k,pos[1])]=="":
                        moves.append((pos[0]+i*k,pos[1]))
                    else:
                        if board[(pos[0]+i*k,pos[1])].color != piece.color:  moves.append((pos[0]+i*k,pos[1]))
                        a=False
                b=True
                for k in range(1,8):
                    if (pos[1]+(i*k) <=8 and pos[1]+(i*k) > 0 and b):
                        if board[(pos[0],pos[1]+i*k)]=="":
                            moves.append((pos[0],pos[1]+i*k))
                        else:
                            if board[(pos[0],pos[1]+i*k)].color != piece.color:  moves.append((pos[0],pos[1]+i*k))
                            b=False
    return list(set(moves))

def king(piece,board):
    moves=[]
    pos=piece.position
    color=piece.color
    for i in [-1,0,1]:
        for j in  [-1,1,0]:
            if i!=0 or j!=0:
                if pos[0]+i in range(1,9) and pos[1]+j in range(1,9):
                    if board[(pos[0]+i,pos[1]+j)]=='' or board[(pos[0]+i,pos[1]+j)].color != color:
                        moves.append((pos[0]+i,pos[1]+j))
    return moves



def knight(piece,board):
    moves=[]
    pos=piece.position
    color=piece.color
    for i in [-2,-1,1,2]:
        for j in [-2,-1,1,2]:
            if not(abs(i)==abs(j)):
                if pos[0]+i in range(1,9) and pos[1]+j in range(1,9):
                    if board[(pos[0]+i,pos[1]+j)]=='' or board[(pos[0]+i,pos[1]+j)].color != color:
                        moves.append((pos[0]+i,pos[1]+j))
    return moves

def castles(board,color="W",side="R"):
    row=1
    if color=="B":row=8



    




