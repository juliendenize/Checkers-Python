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
        self.length = 8
        self.squares = {}
        self.checkers = []
        self.players = [Player('black', 0), Player('white', 1)]
        self.turn = self.players[1]
        self.selectedChecker = None
        self.createSquares()
        self.createCheckers()
        for checker in self.checkers:
            self.computeReachableSquares(checker)
        self.view.canvas.bind("<Button-1>", self.handleCanvasClick)
        self.encodedBoards = [self.encodeBoard()]
    
    def encodeBoard(self):
        code = ""
        for x in range(self.length):
            for y in range(self.length):
                if self.squares[(x,y)].checker:
                    checker = self.squares[(x,y)].checker
                    if checker.player is self.players[0]:
                        if checker.state is State.NORMAL:
                            code += "B"
                        elif checker.state is State.KING:
                            code += "K"
                    else:
                        if checker.state is State.NORMAL:
                            code += "W"
                        elif checker.state is State.KING:
                            code += "Q"
                else:
                    code += "O"
        return code

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
            if(y == self.length // 2 - 1 or y == self.length // 2):
                continue
            for x in range(self.length):
                player = 0
                if(y > self.length // 2):
                    player = 1
                # Only some odd squares contain checkers
                if((x + y) % 2):
                    checker = Checker(x, y, self.players[player],
                                      self.view.createChecker(x, y))
                    self.players[player].checkerNb += 1
                    self.view.colorObject(checker.ui, checker.color)
                    self.checkers.append(checker)
                    self.squares[(x, y)].checker = checker

    def computeAllReachableSquares(self):
        self.players[0].mustAttack = 0
        self.players[1].mustAttack = 0
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
        if checker.state is State.DEAD:
            return

        checker.resetReachableSquares()
        checker.resetJumps()
        for x in range(checker.x - 1, checker.x + 2, 2):
            for y in range(checker.y - 1, checker.y + 2, 2):
                # Check if the coordinates are within the board
                if x >= 0 and x < self.length and y >= 0 and y < self.length:
                    # Check if the coordinates are forward if the checker is not a King
                    if (checker.state is not State.KING) and (self.players[0] is checker.player and y < checker.y or self.players[1] is checker.player and y > checker.y):
                        continue
                    # if there is no checker on the adjacent square
                    if self.squares[(x, y)].checker is None:
                        checker.addReachableSquare(self.squares[(x, y)])
                    # if the checker on the square belongs to the other player
                    elif self.squares[(x, y)].checker is not None and self.squares[(x, y)].checker.player is not checker.player:
                        if x > checker.x and x + 1 < self.length:
                            if y > checker.y and y + 1 < self.length and self.squares[(x+1, y+1)].checker is None:
                                checker.addJump(self.squares[(x+1, y+1)])
                            elif y < checker.y and y - 1 >= 0 and self.squares[(x+1, y-1)].checker is None:
                                checker.addJump(self.squares[(x+1, y-1)])
                        elif x < checker.x and x - 1 >= 0:
                            if y > checker.y and y + 1 < self.length and self.squares[(x-1, y+1)].checker is None:
                                checker.addJump(self.squares[(x-1, y+1)])
                            elif y < checker.y and y - 1 >= 0 and self.squares[(x-1, y-1)].checker is None:
                                checker.addJump(self.squares[(x-1, y-1)])

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
        if self.squares[(x, y)].checker is not None and self.squares[(x, y)].checker.player is self.turn and (not self.turn.mustAttack or (self.turn.mustAttack and self.squares[(x, y)].checker.jumps)):
            checker = self.squares[(x, y)].checker
            if checker.player is self.turn:
                self.selectedChecker = checker
                if checker.jumps:
                    self.selectViewJumpChecker(checker)
                else:
                    self.selectViewReachableChecker(checker)

    def selectViewReachableChecker(self, checker):
        for square in self.selectedChecker.reachableSquares:
            self.view.colorObject(square.ui, "#0000FF")

    def selectViewJumpChecker(self, checker):
        for square in self.selectedChecker.jumps:
            self.view.colorObject(square.ui, "#0000FF")

    def handleCanvasClick(self, event):
        """
            Handle the click event on the canvas

            Arguments
            ----------
            event: object
                the click event
        """
        x = event.x // 80
        y = event.y // 80
        self.makeAction(x,y)
    
    def makeAction(self, x, y):
        if self.selectedChecker is None:
            self.selectChecker(x, y)
        elif self.squares[(x, y)] in self.selectedChecker.jumps:
            self.makeMove(x, y, True)
            self.resetViewSelection()
            # If the checker didn't become a king
            if self.turn.mustAttack:
                self.computeReachableSquares(self.selectedChecker)
                if self.selectedChecker.jumps:
                    self.turn.mustAttack = 2
                    self.selectViewJumpChecker(self.selectedChecker)
                else:
                    self.selectedChecker = None
                    self.computeAllReachableSquares()
                    self.changeTurn()
            else:
                self.selectedChecker = None
                self.computeAllReachableSquares()
                self.changeTurn()
        elif self.squares[(x, y)] in self.selectedChecker.reachableSquares:
            if not self.turn.mustAttack:
                self.makeMove(x, y, False)
                self.resetSelection()
                self.computeAllReachableSquares()
                self.changeTurn()
            else:
                return
        elif self.turn.mustAttack == 2:
            return
        else:
            self.resetSelection()
            self.selectChecker(x, y)

    def changeTurn(self):
        self.turn.time += 1
        old_turn = self.turn
        self.turn = self.players[0] if self.turn is self.players[1] else self.players[1]
        encodedBoard = self.encodeBoard()
        self.encodedBoards.append(encodedBoard)
        if not self.turn.checkerNb or self.turn.mustAttack == -1:
            self.win(old_turn)
        else:
            if len([i for i, x in enumerate(self.encodedBoards) if x == encodedBoard]) > 2:
                self.draw(0)
            elif old_turn.lastNormalPieceMovedMoves >= 40 and self.turn.lastNormalPieceMovedMoves >= 40 and old_turn.lastPieceKilledMoves and self.turn.lastPieceKilledMoves >= 40:
                self.draw(1)
            

    def win(self, player):
        print("win", player.id)
    
    def draw(self, reason):
        print("draw", reason)

    def resetSelection(self):
        self.resetViewSelection()
        self.selectedChecker = None

    def resetViewSelection(self):
        for square in self.selectedChecker.reachableSquares:
            self.view.colorObject(square.ui, square.color)
        for square in self.selectedChecker.jumps:
            self.view.colorObject(square.ui, square.color)

    def makeMove(self, x, y, checkerKilled):
        old_x, old_y = self.selectedChecker.x, self.selectedChecker.y
        self.selectedChecker.x, self.selectedChecker.y = x, y
        self.squares[(x, y)].checker = self.selectedChecker
        self.squares[(old_x, old_y)].checker = None
        self.view.moveChecker(self.selectedChecker.ui, x, y)
        # A checker has been killed
        if checkerKilled:
            if x < old_x and y < old_y:
                killed_x, killed_y = x+1, y+1
            elif x < old_x and y > old_y:
                killed_x, killed_y = x+1, y-1
            elif x > old_x and y < old_y:
                killed_x, killed_y = x-1, y+1
            else:
                killed_x, killed_y = x-1, y-1
            self.killChecker(self.squares[killed_x, killed_y].checker)
            self.turn.lastPieceKilledMoves = 0
        else:
            self.turn.lastPieceKilledMoves +=1
        self.turn.lastNormalPieceMovedMoves = 0 if self.selectedChecker.state is State.NORMAL else self.turn.lastNormalPieceMovedMoves + 1
        if y == 0 and self.turn is self.players[1] or y == self.length-1 and self.turn is self.players[0]:
            self.changeIntoKing(self.selectedChecker)
            # When a piece becomes a king, the player can't play again
            self.turn.mustAttack = 0

    def changeIntoKing(self, checker):
        checker.state = State.KING
        new_ui = self.view.changeIntoKing(
            checker.ui, checker.x, checker.y, checker.color)
        checker.ui = new_ui

    def killChecker(self, checker):
        self.squares[(checker.x, checker.y)].checker = None
        checker.die()
        self.view.killChecker(checker.ui)


master = Tk()
board = Board(master)
master.mainloop()
