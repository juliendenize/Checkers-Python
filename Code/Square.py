class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.checker = None
        self.color = 0 if (x + y) % 2 else 1 
    
    def setChecker(self, checker):
        self.checker = checker