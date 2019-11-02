import torch
import torch.nn as nn
import torch.nn.functional as F


class Agent(nn.Module):
    def __init__(self):
        self.super().__init__()
        self.conv1 = nn.Conv2d(1, 10, 3)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(10, 10, 3)
        self.lstm = nn.LSTMCell(10 * 3 * 3, 256)

    def forward(self, inputs):
        x = self.pool(F.relu(self.conv1(inputs)))
        x = self.pool(F.relu(self.conv2(inputs)))

        return x


class Environment:
    def __init__(self):
        self.length = 8
        self.checkers = 8