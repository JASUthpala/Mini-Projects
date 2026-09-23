import random
import numpy as np
from collections import deque

import torch

from model import Linear_QNet, QTrainer

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):

        self.n_games = 0

        self.epsilon = 0

        self.gamma = 0.9

        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = Linear_QNet(11,256,3)

        self.trainer = QTrainer(
            self.model,
            learning_rate=LR,
            gamma=self.gamma
        )