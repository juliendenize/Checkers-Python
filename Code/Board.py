from Checker import Checker
from Player import Player
from Square import Square
from tkinter import *

class Board:
    def __init__(self):
        self.length = 10
        self.squares = {}
        self.checkers=[]
        self.players = {1: Player('white'), 2: Player('black')}
    
    def createSquares(self):
        for i in range(self.length):
            for j in range(self.length):
                self.squares[(i, j)] = Square(i, j)


    def createCheckers(self):
        for i in range (self.length):
            # Empty rows
            if(i == 5 or i == 6): 
                continue
            for j in range(self.length):
                player = 1
                if(i > 5):
                    player = 2
                # Odd squares contain checkers
                if((i + j) % 2):
                    checker = Checker(i, j, player)
                    self.checkers.append(checker)
                    self.squares[(i, j)].setChecker = checker


    def initBoard(self):
        window = Tk()
        self.createSquares()
        self.createCheckers()
        champ_label = Label(window, text="Salut les Zér0s !")
        champ_label.pack()
        window.mainloop()

board = Board()
board.initBoard()