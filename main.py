from agent import agent
from board import board
from moves import *
from model import Net
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
Agent=agent(board)
def generate_trajectory(actor, max_t=100):
        saved_log_probs = []
        rewards = []
        state_values=[]
        
        
        

        for t in range(max_t):
            
            state=Agent.board_to_array()
            mask,mp=Agent.rel_to_abs_moves()
            action_id, log_prob =  actor.sample(state,mask)
            action=mp[action_id]




            white_reward= Agent.make_move(action['tag'],action['to'],action['castles'])
            if Agent.stalemate("B"):
                print("stalemate game ended")
                rewards.append(-2)
                break
            if Agent.checkmate("B"):
                rewards.append(100)
                break

            # add te obtained results to their relative lists ==> saved_log_probs, rewards, state_values
            tag,to,castles=Agent.sample("B")
            black_reward=Agent.make_move(tag,to,castles)
            if Agent.stalemate("W"):
                print("stalemate game ended")
                rewards.append(2)
                break
            if Agent.checkmate("W"):
                rewards.append(-100)
                break

            # add code here
            saved_log_probs.append(log_prob)
            # add code here
            rewards.append(white_reward - black_reward)
            # add code here


        return  saved_log_probs, rewards, state_values



# print(agent.board)

# agent.make_move("WP5" , (3,5))
# agent.make_move("BP6" , (6,6))
# agent.make_move("WB2" , (2,5))
# agent.make_move("WB2" , (5,8))
# print(agent.isCheck("B"))
# tag,to,castles=agent.sample("B")
# agent.make_move(tag,to,castles)
# print(agent.possible_moves('B'))



# # agent.make_move("WB2" , (2,5))

# rewards=[]
# for _ in range(150):
#     if agent.checkmate("W"):
#         print("checkmate game ended white lose")
#         break
#     if agent.stalemate("W"):
#         print("stalemate game ended")
#         break
#     tag,to,castles=agent.sample("W")
#     reward=agent.make_move(tag,to,castles)
#     rewards.append(reward)
#     if agent.checkmate("B"):
#         print("checkmate game ended black lose")
#         break
#     if agent.stalemate("B"):
#         print("stalemate game ended")
#         break
#     tag,to,castles=agent.sample("B")
#     reward1=agent.make_move(tag,to,castles)
#     rewards.append(reward - reward1)
# print(rewards)

# print("/////////////////////////////////////")

    
    

# agent.make_move("WQ"  , (5,8))


# print(agent.isCheck(color="B"))
# print(agent.possible_moves("B"))







# print(agent.board[(5,8)].possible_moves(agent.board))

# agent.board[(5,8)].possible_moves(agent.board)
# print(agent.rel_to_abs_moves())
# agent.visualize()
model=Net()
# model.forward(sample_input).shape
_,r,_=generate_trajectory(model,max_t=100)
print(r)
Agent.visualize()
