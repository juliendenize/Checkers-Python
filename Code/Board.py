from Checker import Checker
from Player import Player
from Square import Square
from State import State
from tkinter import *

class Board(Frame):
    """
        Principal class of the project. Handle the GUI and the game

        Extends
        ----------
        Frame

        Attributes
        ----------
        canvas : Canvas
            the Canvas that hold the squares and checkers in the UI
        length : int
            the length of the board (10)
        squares : dict(Square)
            the squares composing the board
        players: dict(Player)
            the two players of the game
        checkers: array(Checker)
            the checkers of both players
    """

    def __init__(self, master):
        """
            Construct the board object

            Parameters
            ----------
            master: Tk
                Window of the GUI
        """

        Frame.__init__(self, master)
        master.minsize(width = 700, height = 500)
        self.grid()

        self.length = 10
        self.squares = {}
        self.checkers=[]
        self.players = {1: Player('white'), 2: Player('black')}

        self.initBoard()

    def createSquares(self):
        """
            Create the squares of the board
        """
        for x in range(self.length):
            for y in range(self.length):
                self.squares[(x, y)] = Square(x, y, self.canvas.create_rectangle(x*50, y*50, (x+1)*50, (y+1)*50))
                self.colorObject(self.squares[(x,y)])
    
    def colorObject(self, obj):
        self.canvas.itemconfigure(obj.ui, fill=obj.color)

    def createCheckers(self):
        """
            Create the squares of the board
        """
        for y in range (self.length):
            # Empty rows
            if(y == 4 or y == 5): 
                continue
            for x in range(self.length):
                player = 1
                if(y > 5):
                    player = 2
                # Only some odd squares contain checkers
                if((x + y) % 2):
                    checker = Checker(x, y, player,
                                      self.canvas.create_oval(x*50 + 10, y*50 + 10, (x+1)*50 - 10, (y+1)*50 - 10))
                    self.colorObject(checker)
                    self.checkers.append(checker)
                    self.squares[(x, y)].setChecker(checker)

    def initBoard(self):
        """
            Initialize the board
        """
        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0)

        self.createSquares()
        self.createCheckers()

master = Tk()
board = Board(master)
master.mainloop()