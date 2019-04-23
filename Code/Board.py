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
        players: array(Player)
            the two players of the game
        checkers: array(Checker)
            the checkers of both players
        turn : Player
            the player who is playing
        selectedChecker : Checker
            the checker selected 
    """

    def __str__(self):
        """
            Return the object in string format
        """
        return "Board"

    def __init__(self, master):
        """
            Construct the board object

            Parameters
            ----------
            master: Tk
                Window of the GUI
        """

        Frame.__init__(self, master)
        master.minsize(width=700, height=500)
        self.grid()

        self.length = 10
        self.squares = {}
        self.checkers = []
        self.players = [Player('white'), Player('black')]
        self.turn = self.players[1]
        self.selectedPiece = None

        self.initBoard()

    def createSquares(self):
        """
            Create the squares of the board
        """

        for x in range(self.length):
            for y in range(self.length):
                self.squares[(x, y)] = Square(
                    x, y, self.canvas.create_rectangle(x*50, y*50, (x+1)*50, (y+1)*50))
                self.colorObject(self.squares[(x, y)])

    def colorObject(self, obj):
        """
            Color an object

            Arguments
            ----------
            obj : object
                the object to color

            Raises
            ----------
            AttributeError:
                if the object doesn't have a "ui" or "color" attributes
        """
        if not(hasattr(obj, 'ui') and hasattr(obj, 'color')):
            raise AttributeError(
                'The obj ' + str(board) + ' should have a ui and color property')
        self.canvas.itemconfigure(obj.ui, fill=obj.color)

    def createCheckers(self):
        """
            Create the squares of the board
        """
        for y in range(self.length):
            # Empty rows
            if(y == 4 or y == 5):
                continue
            for x in range(self.length):
                player = 0
                if(y > 5):
                    player = 1
                # Only some odd squares contain checkers
                if((x + y) % 2):
                    checker = Checker(x, y, player,
                                      self.canvas.create_oval(x*50 + 10, y*50 + 10, (x+1)*50 - 10, (y+1)*50 - 10))
                    self.players[player].checkerNb += 1
                    self.colorObject(checker)
                    self.checkers.append(checker)
                    self.squares[(x, y)].setChecker(checker)

    def initBoard(self):
        """
            Initialize the board
        """
        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.bind("<Button-1>", self.handleCanvasClick)
        self.canvas.grid(row=0, column=0)

        self.createSquares()
        self.createCheckers()

    def selectChecker(self, x, y):
        checker = self.squares[(x, y)].checker
        self.selectedChecker = checker

    def handleCanvasClick(self, event):
        """
            Handle the click event on the canvas

            Arguments
            ----------
            event: object
                the click event
        """
        x = event.x // 50
        y = event.y // 50

        if self.selectedChecker is None:
            self.selectChecker(x, y)

        elif (x, y) in self.selectedChecker.reachableSquares:
            self.makeMove(x, y)

    def reachableSquare(self):
        return []

    def makeMove(self, x, y):
        return


master = Tk()
board = Board(master)
master.mainloop()
