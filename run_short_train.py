"""Short training run to verify everything works."""
import train

# Override for quick test
train.NUM_EPISODES = 30
train.PRINT_EVERY = 5
train.SAVE_EVERY = 30
train.MAX_MOVES = 50

train.train()
