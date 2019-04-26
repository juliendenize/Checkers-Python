from Checker import *
from Player import *
from Square import *
from State import *
from View import *
from tkinter import *


class Board():
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
        self.view = View(master)
        self.length = 10
        self.squares = {}
        self.checkers = []
        self.players = [Player('white'), Player('black')]
        self.turn = 1
        self.selectedChecker = None
        self.createSquares()
        self.createCheckers()
        for checker in self.checkers:
            self.computeReachableSquares(checker)
        self.view.canvas.bind("<Button-1>", self.handleCanvasClick)

    def createSquares(self):
        """
            Create the squares of the board
        """
        for x in range(self.length):
            for y in range(self.length):
                self.squares[(x, y)] = Square(
                    x, y, self.view.createSquare(x, y))
                self.view.colorObject(
                    self.squares[(x, y)].ui, self.squares[(x, y)].color)

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
                                      self.view.createChecker(x, y))
                    self.players[player].checkerNb += 1
                    self.view.colorObject(checker.ui, checker.color)
                    self.checkers.append(checker)
                    self.squares[(x, y)].checker = checker

    def computeAllReachableSquares(self):
        for checker in self.checkers:
            self.computeReachableSquares(checker)

    def computeReachableSquares(self, checker):
        """
            Compute all the reachable squares from a checker

            Parameters
            ----------
            checker: Checker
                the checker to compute the reachable squares
        """
        checker.resetReachableSquares()
        if checker.state == State.NORMAL:
            for x in range(checker.x - 1, checker.x + 2, 2):
                for y in range(checker.y - 1, checker.y + 2, 2):
                    # Check if the coordinates are within the board
                    if x >= 0 and x <= 9 and y >= 0 and y <= 9:
                        if (0 == checker.player and y < checker.y) or (1 == checker.player and y > checker.y):
                            continue
                        # if there is no checker on the square
                        if self.squares[(x, y)].checker is None:
                            checker.addReachableSquare(self.squares[(x, y)])
                        # if the checker belongs to the other player
                        elif self.squares[(x, y)].checker.player != checker.player:
                            if x > checker.x and x + 1 <= 9:
                                if y > checker.y and y + 1 <= 9 and self.squares[(x+1, y+1)].checker is None:
                                    checker.addReachableSquare(
                                        self.squares[(x+1, y+1)])
                                elif y < checker.y and y - 1 >= 0 and self.squares[(x+1, y-1)].checker is None:
                                    checker.addReachableSquare(
                                        self.squares[(x+1, y-1)])
                            elif x < checker.x and x - 1 >= 0:
                                if y > checker.y and y + 1 <= 9 and self.squares[(x-1, y+1)].checker is None:
                                    checker.addReachableSquare(
                                        self.squares[(x-1, y+1)])
                                elif y < checker.y and y - 1 >= 0 and self.squares[(x-1, y-1)].checker is None:
                                    checker.addReachableSquare(
                                        self.squares[(x-1, y-1)])
        elif checker.state == State.KING:
            return

    def selectChecker(self, x, y):
        """
            Select the checker given by its coordinates

            Arguments
            ----------
            x : int
                absciss
            y: int
                ordinate
        """
        if (x, y) not in self.squares:
            raise KeyError(
                'The key ' + str(x) + " " + str(y) + " is not in squares")
        if(self.squares[(x, y)].checker is not None and self.squares[(x, y)].checker.player is self.turn):
            checker = self.squares[(x, y)].checker
            if checker.player == self.turn:
                self.selectedChecker = checker
                for square in self.selectedChecker.reachableSquares:
                    self.view.colorObject(square.ui, "#0000FF")

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
        elif self.squares[(x, y)] in self.selectedChecker.reachableSquares:
            self.makeMove(x, y)
            self.resetSelection()
            self.computeAllReachableSquares()
            self.turn = 0 if self.turn else 1
        else:
            self.resetSelection()
            self.selectChecker(x, y)

    def resetSelection(self):
        for square in self.selectedChecker.reachableSquares:
            self.view.colorObject(square.ui, square.color)
        self.selectedChecker = None

    def makeMove(self, x, y):
        old_x, old_y = self.selectedChecker.x, self.selectedChecker.y
        self.selectedChecker.x, self.selectedChecker.y = x,y
        self.squares[(x,y)].checker = self.selectedChecker
        self.squares[(old_x,old_y)].checker = None
        self.view.moveChecker(self.selectedChecker.ui, x, y)
        if self.selectedChecker.state == State.NORMAL:
            # A checker has been killed
            if abs(x-old_x) == 2 and abs(y-old_y) == 2:
                return
        elif self.selectedChecker.state == State.KING:
            return
        return


master = Tk()
board = Board(master)
master.mainloop()
