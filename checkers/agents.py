import pytorch_lightning as pl
from pytorch_lightning import Trainer
import numpy as np

class Agent():
    def __init__(self, seed = None):
        pass

    def act(self, actions):
        raise NotImplementedError

    def update(self, action, reward):
        raise NotImplementedError


class RandomAgent(Agent):
    def __init__(self, seed = None):
        self._rng = np.random.RandomState(seed)
    
    def act(self, actions):
        return self._rng.choice(len(actions))
    
    def update(self, action, reward):
        pass
    

class HistoricalData():
    def __init__(self, X, y, rng):
        self.X = np.asarray(X)
        self.y = np.asarray(y)

        self._rng  = _rng
        self.train = None
        self.val   = None

    def add_data(self, X, y):
        X_prepared = np.asarray(X)
        y_prepared = np.asarray(y)

        self.X = np.concatenate([X, X_prepared])
        self.y = np.concatenate([y, y_prepared])
    
    def prepare_train_val_data(self, percentage_data, percentage_split):
        X, y = rng.shuffle(list(zip(self.X, self.y)))
        
        idx_cut_data = np.ceil(X.shape[0] * percentage_data) 
        X, y = X[:idx_cut_data], y[:idx_cut_data]

        idx_cut_val_train = np.ceil(X.shape[0] * percentage_split)
        X_train, y_train, X_test, y_test = X[:idx_cut_val_train], y[:idx_cut_val_train], X[idx_cut_val_train:], y[idx_cut_val_train:]

        self.train = X_train, y_train
        self.val   = X_test, y_test



class NeuralNet(pl.LightningModule):
    def __init__(self, dataset):
        self.super().__init__()
        self.conv1  = nn.Conv2d(1, 10, 3)
        self.pool   = nn.MaxPool2d(2,2)
        self.conv2  = nn.Conv2d(10, 10, 3)
        self.output = nn.Linear(1)
    
        self.dataset = dataset

    def forward(self, inputs):
        x = self.pool(F.relu(self.conv1(inputs)))
        x = self.pool(F.relu(self.conv2(x)))
        score = self.output(x)
        return score
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.005)

    def train_dataloader(self):
        return DataLoader(self.dataset.train, batch_size = 64)
    
    def val_dataloader(self):
        return DataLoader(self.dataset.val, batch_size = 64)



class DeepAgent(Agent):
    def __init__(self, history, seed = None, online_learning = True, training_step = 1000):
        self._rng    = np.random.RandomState(seed)
        
        self.dataset = HistoricalData(history, self._rng)
        self.model   = NeuralNet()
        self.trainer = Trainer()

        self.online_learning = online_learning
        self.training_step   = training_step

        self.history = []
        self.step = 0

    def init_nn():




    def act(self, actions):

    def update(self, action, reward):
        self.step += 1
        if self.online_learning:
            self.history += [action, reward]
            if self.training_step <= self.step:
                self.step = 0
                
                X = np.asarray([action for action, _ in self.history])
                y = np.asarray([reward for _, reward in self.history])
                self.dataset.add_data(X, y)

                self.trainer.fit(max_epochs = 100)

        
    

