def abs(num):
    if num < 0:
        return -num
    return num
map={}
j=0
for i in range(1,9):    
    map[j]={'tag':"WP"+str(i),'to':(1,0),'castles':''}
    j+=1
    map[j]={'tag':"WP"+str(i),'to':(2,0),'castles':''}
    j+=1
    map[j]={'tag':"WP"+str(i),'to':(1,1),'castles':''}
    j+=1
    map[j]={'tag':"WP"+str(i),'to':(1,-1),'castles':''}
    j+=1

for i in [-1,1]:       
    for k in range(1,8):
                map[j]={'tag':"WQ",'to':(i*k,0),'castles':''}
                j=j+1
                map[j]={'tag':"WQ",'to':(0,i*k),'castles':''}
                j=j+1
                for m in range(1,9):
                    map[j]={'tag':"WQ"+str(m),'to':(i*k,0),'castles':''}
                    j=j+1
                    map[j]={'tag':"WQ"+str(m),'to':(0,i*k),'castles':''}
                    j=j+1
                     
                map[j]={'tag':"WR1",'to':(i*k,0),'castles':''}
                j=j+1
                map[j]={'tag':"WR1",'to':(0,i*k),'castles':''}
                j=j+1
                map[j]={'tag':"WR2",'to':(i*k,0),'castles':''}
                j=j+1
                map[j]={'tag':"WR2",'to':(0,i*k),'castles':''}
                j=j+1
for i in [-1,1]: 
    for l in [-1,1]:           
        for k in range(1,8):
                map[j]={'tag':"WQ",'to':(i*k,l*k),'castles':''}
                j=j+1
                for m in range(1,9):
                     map[j]={'tag':"WQ"+str(m),'to':(i*k,l*k),'castles':''}
                     j=j+1
                     
                map[j]={'tag':"WB1",'to':(i*k,l*k),'castles':''}
                j=j+1
                map[j]={'tag':"WB2",'to':(i*k,l*k),'castles':''}
                j=j+1
for i in [-2,-1,1,2]:
    for l in [-2,-1,1,2]:
        if not(abs(i)==abs(l)):
             map[j]={'tag':"WN1",'to':(i,l),'castles':''}
             j+=1
             map[j]={'tag':"WN2",'to':(i,l),'castles':''}
             j+=1
for i in [-1,0,1]:
        for l in  [-1,1,0]:
            if i!=0 or j!=0: 
                map[j]={'tag':"WK",'to':(i,l),'castles':''}
                j+=1   
map[j]={'tag':"WK",'to':(1,7),'castles':'R'}
j+=1
map[j]={'tag':"WK",'to':(1,3),'castles':'L'}     
              

