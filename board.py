from piece import piece
board={}
for i in range(1,9):
    for j in range(1,9):
        board[(i,j)]=''


for i in range(1,9):
    board[(2,i)]=piece(piece="P",color="W",moved=False,position=(2,i),tag="WP"+str(i))
    board[(7,i)]=piece(piece="P",color="B",moved=False,position=(7,i),tag="BP"+str(i))


board[(1,1)]=piece(piece="R",color="W",moved=False,position=(1,1),tag="WR1")
board[(8,1)]=piece(piece="R",color="B",moved=False,position=(8,1),tag="BR1")

board[(1,2)]=piece(piece="N",color="W",moved=False,position=(1,2),tag="WN1")
board[(8,2)]=piece(piece="N",color="B",moved=False,position=(8,2),tag="BN1")

board[(1,3)]=piece(piece="B",color="W",moved=False,position=(1,3),tag="WB1")
board[(8,3)]=piece(piece="B",color="B",moved=False,position=(8,3),tag="BB1")

board[(1,4)]=piece(piece="Q",color="W",moved=False,position=(1,4),tag="WQ")
board[(8,4)]=piece(piece="Q",color="B",moved=False,position=(8,4),tag="BQ")

board[(1,5)]=piece(piece="K",color="W",moved=False,position=(1,5),tag="WK")
board[(8,5)]=piece(piece="K",color="B",moved=False,position=(8,5),tag="BK")

board[(1,6)]=piece(piece="B",color="W",moved=False,position=(1,6),tag="WB2")
board[(8,6)]=piece(piece="B",color="B",moved=False,position=(8,6),tag="BB2")

board[(1,7)]=piece(piece="N",color="W",moved=False,position=(1,7),tag="WN2")
board[(8,7)]=piece(piece="N",color="B",moved=False,position=(8,7),tag="BN2")

board[(1,8)]=piece(piece="R",color="W",moved=False,position=(1,8),tag="WR2")
board[(8,8)]=piece(piece="R",color="B",moved=False,position=(8,8),tag='BR2')

tags=[
    "WP1","WP2","WP3","WP4","WP5","WP6","WP7","WP8","WR1","WR2","WB1","WB2","WN1","WN2","wQ","WK",
    "BP1","BP2","BP3","BP4","BP5","BP6","BP7","BP8","BR1","BR2","BB1","BB2","BN1","BN2","BQ","BK"
    ]