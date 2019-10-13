from board import Board
from tkinter import Tk
from view import FirstMenu

class Controller():
    def __init__(self, master):
        assert isinstance(master, Tk), "'master' must be an instance of Tk"
        self.master = master
    
    def displayFirstMenu(self):
        FirstMenu(self)

    def startGame(self, type):
        """
            Start the game by calling the board and then let the board taking care of the game(s).
        """
        self.board = Board(self)