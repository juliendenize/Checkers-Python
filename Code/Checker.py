from State import *


class Checker:
    """
        Represent a checker object

        Attributes
        ----------
        x : int
             Absciss
        y : int
            ordinate
        player : Player
            the player owning the checker
        state : State
            the state of the checker
        color : string
            color of the checker
        ui : int
            id of the checker for the board canvas
        reachableSquares : array(Squares)
            the squares reachable from this checker
    """

    def __init__(self, x, y, player, ui):
        """
            Construct the Checker object

            Parameters
            ----------
            x : int
                absciss
            y : int
                ordinate
            player : Player
                the player
            ui : int
                the ui id
        """

        self.x = x
        self.y = y
        self.player = player
        self.state = State.NORMAL
        self.color = "#FFFFFF" if player == 1 else "#FF0000"
        self.ui = ui
        self.reachableSquares = []

    def resetReachableSquares(self):
        """
            Reset the reachable squares attributes
        """
        self.reachableSquares = []

    def addReachableSquare(self, square):
        """
            Add a reachable square

            Parameters
            ----------
            square : Square
                the square to add
        """
        self.reachableSquares.append(square)
