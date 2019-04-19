from State import State

class Checker:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.state = State.NORMAL