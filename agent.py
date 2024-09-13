import numpy as np
import matplotlib.pyplot as plt
import copy
from utils.model_env_map import map
from utils.one_hot_encode import hot_encode
import torch
class agent():
    def __init__(self,board):
        self.board=board
        self.reset=board  

    def get_position(self,tag):
        for square in self.board:
            if self.board[square] !="":
                if self.board[square].tag == tag:
                    return square
                
    def isCheck(self,color="W",sq=""):
        """
        Checks whether a player's king is under attack or not.
        or check any given square is under attack (used to check possibility for castles as the path should be safe
        """


        if color=="W":tag="WK"
        else:tag="BK"
        if sq !="":pos=sq
        else:pos=self.get_position(tag)
        
        for square in self.board:
            if self.board[square] !="":
                possible_moves=self.board[square].possible_moves(self.board)
                if self.board[square] !="" and self.board[square].color != color:
                    if not len(possible_moves)==0 and  pos in possible_moves  :return True
        return False
    def checkmate(self,color="W"):
        if (self.isCheck(color)) and self.possible_moves(color)==[]:return True
    def stalemate(self,color="W"):
        if self.possible_moves(color)==[]:return True
        return False


    def is_legit(self,move):
        pass
    
    def make_move(self,tag,to,castles=''):
        """ 
        It returns the updated board if the move is legit else it returs False
                                                    
        """
        reward=0.5
        piece=self.board[self.get_position(tag)]
        position=self.get_position(tag)
        color= "B" if tag[0]=="W" else "W"
        board=self.board
        if not piece.captured and (to in piece.possible_moves(self.board) or (     castles !=''and self.castles (tag[0],castles))) :
            if self.board[to]!="":
                self.board[to].captured=True
                reward+=self.board[to].score()
            self.board[to]=piece
            self.board[position]=""
            self.board[to].position=to
            self.board[to].moved=True
            if castles!='':
                reward+=2
                row=to[0]
                if castles =="R":
                    print("king side castle")
                    #king side castle
                    self.board[(row,6)]=self.board[row,8]
                    self.board[(row,6)].moved=True
                    self.board[(row,8)]=""
                    
                else:
                    print("king side castle")
                    #queen side castle
                    self.board[(row,3)]=self.board[row,1]
                    self.board[(row,3)].moved=True
                    self.board[(row,1)]=""
                    
            #promote
            if tag[:2]=="WP" and to[0]==8:
                self.board[to].tag="WQ"+tag[-1]
                self.board[to].piece="Q"
                reward=reward + 50
            if tag[:2]=="BP" and to[0]==1:
                self.board[to].tag="BQ"+tag[-1]
                self.board[to].piece="Q"
                reward= reward + 50
            
            # if self.isCheck(color):reward += 1.5
            # if self.checkmate(color):reward += 1.0
            # if self.stalemate(color):reward=0
            
        return reward
    def castles(self,color="W",side="R"):
        
        row=1
        if color=="B":row=8
        if side=="R":
            
            if not(self.board[(row,5)].moved):
                if not(self.isCheck(color,sq=(row,6))) and not(self.isCheck(color,sq=(row,7))) and self.board[(row,8)]!='' and not(self.board[(row,8)].moved):
                    if (self.board[(row,6)]=="") and  (self.board[(row,7)]=="") :return True
        else:
            if not(self.board[(row,5)].moved):
                if not(self.isCheck(color,sq=(row,4))) and not(self.isCheck(color,sq=(row,3))) and self.board[(row,1)]!='' and not(self.board[(row,1)].moved):
                    if (self.board[(row,4)]=="") and  (self.board[(row,3)]=="") :return True

        return False
        
    

    def board_to_array(self):
        arr=np.zeros((6,8,8))
        a={
            "R":0,
            "N":1,
            "B":2,
            "K":3,
            "Q":4,
            "P":5
        }
        for sq,piece in zip(self.board.keys(),self.board.values()):
            if piece != "":
                i=a[piece.piece]
                j=1
                if piece.color == "B":j=-1
                arr[i,sq[0]-1,sq[1]-1]=j
        return arr
            

    def possible_moves(self,Color_to_move):
        all=[]
        color= "B" if Color_to_move=="W" else "W"
        if (self.isCheck(Color_to_move)):
            tmp=copy.deepcopy(self.board)
            tmp_board=tmp

            tmp_agent=agent(tmp_board)
            for piece in self.board.values():
                if piece != "" and piece.color == Color_to_move:
                    piece_possible_moves=piece.possible_moves(self.board)
                    for move in piece_possible_moves:
                        tmp_agent.make_move(tag=piece.tag,to=move)
                        if not(tmp_agent.isCheck(Color_to_move)):
                            all.append({"tag":piece.tag,'to':move,'castles':''})
                            
                        tmp_board=copy.deepcopy(self.board)
                        tmp_agent=agent(tmp_board)
        else:
            for piece in self.board.values():
                tmp=copy.deepcopy(self.board)
                tmp_board=tmp
                tmp_agent=agent(tmp_board)

                if piece != "" and piece.color == Color_to_move:
                    # print("this is tag",piece.tag)
                    piece_possible_moves=piece.possible_moves(self.board)
                    for i in piece_possible_moves:
                        tmp_agent.make_move(piece.tag , i)
                        if not (tmp_agent.isCheck(Color_to_move)) :
                            all.append({"tag":piece.tag,'to':i,'castles':''})
                        tmp=copy.deepcopy(self.board)
                        tmp_board=tmp
                        tmp_agent=agent(tmp_board)
                    
        row = 1 if Color_to_move=="W" else 8 
        if  self.board[row,5]!=''  and self.board[row,5].piece == 'K':
            if self.castles(Color_to_move,"R"):all.append({'tag':Color_to_move+"K",'to':(row,7),'castles':"R"})
            if self.castles(Color_to_move,"L"):all.append({'tag':Color_to_move+"K",'to':(row,7),'castles':"L"})
                    
            
        return all
    
    def sample(self,color):
        moves=self.possible_moves(color)
        n=len(moves)
        scores = np.zeros(n)
        for i in range(n):
            to=moves[i]['to']
            if self.board[to]!='':scores[i]=self.board[to].score()

        if sum(scores)==0:move=np.random.choice(moves)
        else:
            scores=torch.from_numpy(scores).float()
            id = torch.multinomial(scores,1)[0].item()
            move=moves[id]
        return move['tag'],move['to'],move['castles']
    
    def stockfich_format(self , tag , to ):
        pass
                    


    def visualize(self):
        board = np.zeros((8,8,3))
        board[::2, 1::2] = [255,255,255]
        board[1::2, ::2] = [255,255,255]
        fig, ax = plt.subplots()

        # Draw the chess board
        ax.imshow(board, origin='lower', extent=(0, 8, 0, 8))
        for i in range(1,9):
            for j in range(1,9):
                if (self.board[(i, j)] != ''):
                    ax.text( j - 0.8 , i - 0.8 , self.board [ ( i , j ) ].tag , color='blue')
        plt.show()
    
    def rel_to_abs_moves(self,color="W"):
        mp=copy.deepcopy(map)
        pos={}
        for sq,piece in zip(self.board.keys(),self.board.values()):
            if piece !="" and piece.color==color:
                pos[piece.tag]=sq
        for i,rel in zip(map.keys(),map.values()):
            if mp[i]['tag'] in pos:
                if mp[i]['castles']=="":
                    mp[i]['to'] = (mp[i]['to'][0]+pos[mp[i]['tag']][0],mp[i]['to'][1]+pos[mp[i]['tag']][1])  
        mask=[]
        possible_moves=self.possible_moves(color)
        for i in mp.values():
            if (i in possible_moves): 
                mask.append(1)
            else : mask.append(0) 
        return torch.from_numpy(np.array(mask)),mp

    def abs_to_rel_moves(self,tag,to,castles):
        pos=self.get_position(tag)
        rel=(to[0]-pos[0],to[1]-pos[1])
        rel_pos={"tag":tag,"to":rel,"castles":castles}
        for k,v in zip (map.keys(),map.values()):
            if v==rel_pos:return(k)

    
    
        
    