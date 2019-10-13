from classes import Square, Checker, State, Player
from view import BoardView
import top_controller


class Board():
    """
        Principal class of the project. Handle the GUI and the game

        Extends
        ----------
        Frame

        Attributes
        ----------
        view : BoardView
            the frame that holds the UI of the game (board + scores)
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
        encodedBoards: array(String)
            each turn encoded in String
    """

    def __str__(self):
        """
            Return the object in string format
        """
        return "Board"

    def __init__(self, controller):
        """
            Construct the board object

            Parameters
            ----------
            master: Tk
                Window of the GUI
        """
        assert isinstance(controller, top_controller.Controller), "'controller' must be an instance of Controller"
        self.controller = controller
        self.view = BoardView(self.controller.master)
        self.view.board.bind("<Button-1>", self.handleCanvasClick)

        self.length = 8
        self.squares = {}
        self.checkers = []
        self.players = [Player('black', 0), Player('white', 1)]
        self.turn = self.players[1]
        self.selectedChecker = None
        
        self.createSquares()
        self.createCheckers()
        self.computeAllMoves()
        
        self.encodedBoards = [self.encodeBoard()]

    def encodeBoard(self):
        """
            Encode the current board in String format

            Return
            ----------
            String: the board encoded
        """
        code = ""
        for x in range(self.length):
            for y in range(self.length):
                if self.squares[(x, y)].checker:
                    checker = self.squares[(x, y)].checker
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
                    code += "x"
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

    def computeAllMoves(self):
        """
            Compute all the moves possible
        """
        self.players[0].mustAttack = 0
        self.players[1].mustAttack = 0
        for checker in self.checkers:
            self.computeMoves(checker)

    def computeMoves(self, checker):
        """
            Compute all moves from a checker

            Parameters
            ----------
            checker: Checker
                the checker to compute the reachable squares
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

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
        """
            Color the view selection of reachable adjacent squares (color in blue)
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

        for square in self.selectedChecker.reachableSquares:
            self.view.colorObject(square.ui, "#0000FF")

    def selectViewJumpChecker(self, checker):
        """
            Color the view selection of jumps (color in blue)
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

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
        if self.selectedChecker is None:
            self.selectChecker(x, y)
        elif self.squares[(x, y)] in self.selectedChecker.jumps:
            self.jump(x, y)
        elif self.squares[(x, y)] in self.selectedChecker.reachableSquares:
            if not self.turn.mustAttack:
                self.simpleMove(x, y)
            else:
                return
        elif self.turn.mustAttack == 2:
            return
        else:
            self.resetSelection()
            self.selectChecker(x, y)

    def jump(self, x, y):
        """
            Make the jump of a checker

            Arguments
            ----------
            x: int
                The absiss position to jump
            y: int
                The ordinate position to jump
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        # kill the checker jumped
        if x < self.selectedChecker.x and y < self.selectedChecker.y:
            killed_x, killed_y = x+1, y+1
        elif x < self.selectedChecker.x and y > self.selectedChecker.y:
            killed_x, killed_y = x+1, y-1
        elif x > self.selectedChecker.x and y < self.selectedChecker.y:
            killed_x, killed_y = x-1, y+1
        else:
            killed_x, killed_y = x-1, y-1
        self.killChecker(self.squares[killed_x, killed_y].checker)
        self.turn.lastJumpMoves = 0

        self.makeMove(x, y)
        self.resetViewSelection()
        self.updateViewScores()
        # If the checker didn't become a king
        if self.turn.mustAttack:
            self.computeMoves(self.selectedChecker)
            if self.selectedChecker.jumps:
                self.turn.mustAttack = 2
                self.selectViewJumpChecker(self.selectedChecker)
            else:
                self.selectedChecker = None
                self.computeAllMoves()
                self.changeTurn()
        # Else the turn must change
        else:
            self.selectedChecker = None
            self.computeAllMoves()
            self.changeTurn()

    def simpleMove(self, x, y):
        """
            Move the checker to an ajdacent position

            Arguments
            ----------
            x: int
                The absiss position to move
            y: int
                The ordinate position to move
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        self.turn.lastJumpMoves += 1
        self.makeMove(x, y)
        self.resetSelection()
        self.computeAllMoves()
        self.changeTurn()

    def changeTurn(self):
        """
            Change the player turn
        """
        self.turn.time += 1
        old_turn = self.turn
        self.turn = self.players[0] if self.turn is self.players[1] else self.players[1]
        encodedBoard = self.encodeBoard()
        self.encodedBoards.append(encodedBoard)
        if not self.turn.checkerNb or self.turn.mustAttack == -1:
            self.win(old_turn)
        else:
            if len([i for i, code in enumerate(self.encodedBoards) if code == encodedBoard]) > 2:
                self.draw(False)
            elif old_turn.lastNormalPieceMovedMoves >= 40 and self.turn.lastNormalPieceMovedMoves >= 40 and old_turn.lastJumpMoves and self.turn.lastJumpMoves >= 40:
                self.draw(True)

    def win(self, player):
        """
            Declare the player winner

            Arguments
            ----------
            player: Player
                The winner
        """

        assert isinstance(
            player, Player), "'player' must be an instance of Player"

        print("win", player.id)

    def draw(self, reason):
        """
            Declare it is a draw

            Arguments
            ----------
            reason: boolean
                The reason why it is a draw: 0 if the board was the same 3 times, 1 if no piece were killed or normal piece was moved for 40 round for each player
        """
        assert type(reason) is bool, "'reason' must be a boolean."

        print("draw", reason)

    def resetSelection(self):
        """
            Reset the selection of a piece
        """
        self.resetViewSelection()
        self.selectedChecker = None

    def resetViewSelection(self):
        """
            Reset the view selection (blue squares back to normal)
        """
        for square in self.selectedChecker.reachableSquares:
            self.view.colorObject(square.ui, square.color)
        for square in self.selectedChecker.jumps:
            self.view.colorObject(square.ui, square.color)

    def makeMove(self, x, y):
        """
            Move the selected checker to a new position

            Arguments
            ----------
            x: int
                The absiss position
            y: int
                The ordinate position
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        old_x, old_y = self.selectedChecker.x, self.selectedChecker.y
        self.selectedChecker.x, self.selectedChecker.y = x, y
        self.squares[(x, y)].checker = self.selectedChecker
        self.squares[(old_x, old_y)].checker = None
        self.view.moveChecker(self.selectedChecker.ui, x, y)
        self.turn.lastNormalPieceMovedMoves = 0 if self.selectedChecker.state is State.NORMAL else self.turn.lastNormalPieceMovedMoves + 1
        if y == 0 and self.turn is self.players[1] or y == self.length-1 and self.turn is self.players[0]:
            self.changeIntoKing()
            # When a piece becomes a king, the player can't play again
            self.turn.mustAttack = 0

    def changeIntoKing(self):
        """
            Change into a king the selected checker
        """
        self.selectedChecker.state = State.KING
        new_ui = self.view.changeIntoKing(
            self.selectedChecker.ui, self.selectedChecker.x, self.selectedChecker.y, self.selectedChecker.color)
        self.selectedChecker.ui = new_ui

    def killChecker(self, checker):
        """
            Kill the checker given

            Arguments
            ----------
            checker: Checker
                The checker to kill
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

        self.squares[(checker.x, checker.y)].checker = None
        checker.die()
        self.view.killChecker(checker.ui)

    def updateViewScores(self):
        self.view.updateScores(self.players[1].checkerNb, self.players[0].checkerNb)
