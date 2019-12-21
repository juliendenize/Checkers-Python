import torch
import torch.nn as nn
import torch.nn.functional as F
import Board from Board


actions_size = 96


class Agent(nn.Module):
    def __init__(self):
        self.super().__init__()
        self.conv1 = nn.Conv2d(1, 10, 3)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(10, 10, 3)
        self.output_actions = nn.Linear(actions_size)

    def forward(self, inputs):
        x = self.pool(F.relu(self.conv1(inputs)))
        x = self.pool(F.relu(self.conv2(x)))
        return x
