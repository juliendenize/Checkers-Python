class Square:
    def __init__(self, x, y, ui):
        self.x = x
        self.y = y
        self.checker = None
        self.color = "#000000" if (x + y) % 2 else "#FA6565"
        self.ui = ui      
    
    def setChecker(self, checker):
        self.checker = checker