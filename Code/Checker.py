from State import State

class Checker:
    def __init__(self, x, y, player, ui):
        self.x = x
        self.y = y
        self.player = player
        self.state = State.NORMAL
        self.color = "#FFFFFF" if player == 1 else "#FF0000"
        self.ui = ui