from agent import agent
import torch
import numpy as np
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
from agent import agent
# from utils.model_env_map import map

# PyTorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(6, 32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(128 * 1 * 1, 256)
        self.relu4 = nn.ReLU()
        self.fc2 = nn.Linear(256, 675)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.pool3(self.relu3(self.conv3(x)))
        
        # Flatten the output before fully connected layers
        x = x.view(-1, 128 * 1 * 1)
        
        # Fully connected layers
        x = self.relu4(self.fc1(x))
        x = self.fc2(x)
        
        # Apply softmax activation to convert raw scores into probabilities
        x = F.softmax(x, dim=1)
        
        return x
    
    def sample(self,x,mask):
        x = torch.from_numpy(x).float().unsqueeze(0)

        probs = self.forward(x).squeeze()
        probs = probs * mask
        m = Categorical(probs)
        action = m.sample()
        return action.item() , m.log_prob(action)
        



