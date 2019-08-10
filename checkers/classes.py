from enum import Enum


class Square:
    """
        Represent a checker object

        Attributes
        ----------
        x : int
             Absciss
        y : int
            ordinate
        checker: @Checker
            the checker hold by the square
        color : string
            color of the square
        ui : int
            id of the checker for the board canvas
    """

    def __init__(self, x, y, ui):
        """
            Construct the Square object

            Parameters
            ----------
            x : int
                absciss
            y : int
                ordinate
            ui : int
                the ui id
        """

        assert type(x) is int, "'x' must be an integer"
        assert type(y) is int, "'y' must be an integer"
        assert type(ui) is int, "'ui' must be an integer"

        self.x = x
        self.y = y
        self.checker = None
        self.color = "#000000" if (x + y) % 2 else "#FA6565"
        self.ui = ui


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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"
        assert isinstance(player, Player), "'player' must be a Player"
        assert type(ui) is int, "'ui' must be an integer"

        self.x = x
        self.y = y
        self.player = player
        self.state = State.NORMAL
        self.color = "#FFFFFF" if self.player.id == 1 else "#FF0000"
        self.ui = ui
        self.reachableSquares = []
        self.jumps = []

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

        assert isinstance(square, Square), "'square' must be a Square"

        self.reachableSquares.append(square)

    def resetJumps(self):
        """
            Reset the reachable squares attributes
        """
        self.jumps = []

    def addJump(self, square):
        """
            Add a reachable square

            Parameters
            ----------
            square : Square
                the square to add
        """

        assert isinstance(square, Square), "'square' must be a Square"

        self.jumps.append(square)
        self.player.mustAttack = 1

    def die(self):
        """
            Kill this checker
        """
        self.state = State.DEAD
        self.player.checkerNb -= 1


class State(Enum):
    """
        Represent a State object for checkers

        Extends
        ----------
        Enum

        Values
        ----------
        NORMAL:
            checker is no king and alive
        KING:
            checker is a king
        DEAD:
            checker is dead
    """
    NORMAL = 1
    KING = 2
    DEAD = 3


class Player:
    """
        Represent a player object

        Attributes
        ----------
        name: string
            the name of the player
        id: int
                the id of the player (0 or 1)
        time: Time
            the time the player played
        checkerNb: int
            the number of checkers alive
        mustAttack: int
            -1 if the player can't move, 0 if the player can't jump, 1 if he can jump, 2 if he can jump and already jumped
        lastNormalPieceMovedMoves: int
            number of moves since the player didn't move a normal piece
        lastJumpMoves: int
            number of moves since the player didn't jump
    """

    def __init__(self, name, id):
        """
            Construct the player object

            Parameters
            ----------
            name: string
                the name of the player
            id: int
                the id of the player (0 or 1)
        """

        assert type(name) is str, "'name' must be a string"
        assert type(id) is int, "'id' must be an integer"

        self.name = name
        self.time = 0
        self.id = id
        self.checkerNb = 0
        self.mustAttack = 0
        self.lastNormalPieceMovedMoves = 0
        self.lastJumpMoves = 0
