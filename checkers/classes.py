from enum import Enum


class Square:
    """
        Represent a checker object

        Attributes
        ----------
        x : int
             Abscissa
        y : int
            ordinate
        checker: @Checker
            the checker hold by the square
        color : string
            color of the square
        ui : int
            id of the checker for the board canvas
    """

    def __init__(self, x, y):
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

        self.x = x
        self.y = y
        self.checker = None
        self.color = "#000000" if (x + y) % 2 else "#FA6565"
        self.ui = None


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
        reachable_squares : array(Squares)
            the squares reachable from this checker
        id : int
            id of the checker to identify itself
        in_danger: boolean
            True if the checker is killable
    """

    def __init__(self, x, y, player, id):
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
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"
        assert isinstance(player, Player), "'player' must be a Player"

        self.x = x
        self.y = y
        self.player = player
        self.state = State.NORMAL
        self.color = "#FFFFFF" if self.player.id == 1 else "#FF0000"
        self.ui = None
        self.id = id
        self.reachable_squares = []
        self.jumps = []
        self.in_danger = False

    def reset_reachable_squares(self):
        """
            Reset the reachable squares attributes
        """
        self.reachable_squares = []

    def add_reachable_square(self, square):
        """
            Add a reachable square

            Parameters
            ----------
            square : Square
                the square to add
        """

        assert isinstance(square, Square), "'square' must be a Square"

        self.reachable_squares.append(square)

    def reset_jumps(self):
        """
            Reset the reachable squares attributes
        """
        self.jumps = []

    def add_jump(self, square):
        """
            Add a reachable square by jump

            Parameters
            ----------
            square : Square
                the square to add
        """

        assert isinstance(square, Square), "'square' must be a Square"

        self.jumps.append(square)
        self.player.must_attack = 1

    def die(self):
        """
            Kill this checker
        """
        self.player.checker_nb -= 1
        if self.state == State.KING:
            self.player.king_nb -= 1

        self.state = State.DEAD
        


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


class GameState(Enum):
    """
        Represent a game state object for board

        Extends
        ----------
        Enum

        Values
        ----------
        IN_PROGRESS:
            game in progress    
        DRAW:
            draw
        WIN_WHITE:
            win for white side
        WIN_BLACK:
            win for back side
    """
    IN_PROGRESS = 0
    DRAW        = 1
    WIN_WHITE   = 2
    WIN_BLACK   = 3


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
        ai: boolean
            true if the player is an ai
        checker_nb: int
            the number of checkers alive
        must_attack: int
            - -1 if the player can't move
            - 0 if the player can't jump
            - 1 if he can jump
            - 2 if he can jump and already jumped
        last_normal_piece_moved_moves: int
            number of moves since the player didn't move a normal piece
        last_jump_moves: int
            number of moves since the player didn't jump
        checkers: list[Checkers]
            list of the checkers belonging to this player
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

        self.name        = name
        self.time        = 0
        self.id          = id
        self.checker_nb  = 0
        self.king_nb     = 0
        self.must_attack = 0
        
        self.last_normal_piece_moved_moves = 0
        self.last_jump_moves = 0
        
        self.checkers  = []
        self.ai        = False
        self.killables = []
        self.killable_kings   = 0
        self.killable_normals = 0
    
    def reset_killable(self):
        self.killables        = []
        self.killable_kings   = 0
        self.killable_normals = 0
    
    def add_killable(self, checker):
        if checker not in killables:
            self.killables += checker
            if checker.state == State.KING:
                self.killable_kings += 1
            else:
                self.killable_normals += 1
        return
