from classes import Square, Checker, State, Player, GameState
from view import BoardView
import top_controller
import numpy as np
import copy


class Board:
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
        selected_checker : Checker
            the checker selected
        encodedBoards: dict(String: int)
            each board configuration encoded in String associated with occurences
        game_state: GameState
            state of the game
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
            controller: Tk
                Window of the GUI
        """

        assert controller is not None, "'controller' must not be None"
        self.controller = controller
        self.length = 8
        
        if self.controller is not "copy": 
            self.init()

  
    def init(self):
        self.squares = {}
        self.checkers = []
        self.players = [Player('black', 0), Player('white', 1)]
        self.turn = self.players[1]
        self.selected_checker = None
        self.game_state = GameState.IN_PROGRESS

        if isinstance(controller, self.top_controller.Controller):
            self.view = BoardView(self.controller.master)
            self.view.board.bind("<Button-1>", self.handle_canvas_click)

        else:
            # it means the AI is using the board as an environment and doesnt require a view.
            # This variable helps to construct the board without displaying a UI.
            self.view = None
            self.players[0].ai = True
            self.players[1].ai = True


        self.create_squares()
        self.create_checkers()

        self.compute_all_moves()

        self.encodedBoards = {self.encode_board(): 1}

    def encode_board_np(self):
        """
            Encode the current board in Numpy format

            Return
            ----------
            np.ndarray: the board encoded
        """
        code = np.zeros((self.length, self.length))
        for x in range(self.length):
            for y in range(self.length):
                if self.squares[(x, y)].checker is not None:
                    checker = self.squares[(x, y)].checker
                    if checker.player is self.players[1]:
                        if checker.state is State.NORMAL:
                            code[y][x] = 1
                        elif checker.state is State.KING:
                            code[y][x] = 2
                    else:
                        if checker.state is State.NORMAL:
                            code[y][x] = -1
                        elif checker.state is State.KING:
                            code[y][x] = -2
        return code


    def encode_board(self):
        """
            Store the board in the encoded board dict

            Return
            ----------
            None
        """
        code = ""
        for x in range(self.length):
            for y in range(self.length):
                if self.squares[(x, y)].checker is not None:
                    checker = self.squares[(x, y)].checker
                    if checker.player is self.players[1]:
                        if checker.state is State.NORMAL:
                            code += "1"
                        elif checker.state is State.KING:
                            code += "2"
                    else:
                        if checker.state is State.NORMAL:
                            code += "-1"
                        elif checker.state is State.KING:
                            code += "-2"
                else:
                    code += "0"
        return code


    def create_squares(self):
        """
            Create the squares of the board
        """
        for x in range(self.length):
            for y in range(self.length):
                self.squares[(x, y)] = Square(x, y)

                if self.view is not None:
                    self.squares[(x, y)].ui = self.view.create_square(x, y)
                    self.view.color_object(
                        self.squares[(x, y)].ui, self.squares[(x, y)].color)


    def create_checkers(self):
        """
            Create the squares of the board
        """
        for y in range(self.length):
            # Empty rows
            if y == self.length // 2 - 1 or y == self.length // 2:
                continue
            for x in range(self.length):
                player = 0
                if y > self.length // 2:
                    player = 1
                # Only some odd squares contain checkers
                if (x + y) % 2:
                    self.players[player].checker_nb += 1
                    checker = Checker(x, y, self.players[player], self.players[player].checker_nb)
                    self.players[player].checkers.append(checker)

                    if self.view is not None:
                        checker.ui = self.view.create_checker(x, y)
                        self.view.color_object(checker.ui, checker.color)

                    self.checkers.append(checker)
                    self.squares[(x, y)].checker = checker


    def compute_all_moves(self):
        """
            Compute all the moves possible
        """
        self.players[0].reset_killable()
        self.players[1].reset_killable()
        for checker in self.checkers:
            self.compute_checker_moves(checker)


    def compute_checker_moves(self, checker):
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

        checker.reset_reachable_squares()
        checker.reset_jumps()
        for x in range(checker.x - 1, checker.x + 2, 2):
            for y in range(checker.y - 1, checker.y + 2, 2):
                # Check if the coordinates are within the board
                if 0 <= x < self.length and 0 <= y < self.length:
                    # Check if the coordinates are forward if the checker is not a King
                    if (checker.state is not State.KING) and (self.players[0] is checker.player and y < checker.y or
                                                              self.players[1] is checker.player and y > checker.y):
                        continue
                    # if there is no checker on the adjacent square
                    if self.squares[(x, y)].checker is None:
                        checker.add_reachable_square(self.squares[(x, y)])
                    # if the checker on the square belongs to the other player
                    elif self.squares[(x, y)].checker is not None and \
                            self.squares[(x, y)].checker.player is not checker.player:
                        if x > checker.x and x + 1 < self.length:
                            if y > checker.y and y + 1 < self.length and self.squares[(x + 1, y + 1)].checker is None:
                                checker.add_jump(self.squares[(x + 1, y + 1)])
                                checker.player.add_killable(self.squares[(x, y)].checker)
                            elif y < checker.y and y - 1 >= 0 and self.squares[(x + 1, y - 1)].checker is None:
                                checker.add_jump(self.squares[(x + 1, y - 1)])
                                checker.player.add_killable(self.squares[(x, y)].checker)
                        elif x < checker.x and x - 1 >= 0:
                            if y > checker.y and y + 1 < self.length and self.squares[(x - 1, y + 1)].checker is None:
                                checker.add_jump(self.squares[(x - 1, y + 1)])
                                checker.player.add_killable(self.squares[(x, y)].checker)
                            elif y < checker.y and y - 1 >= 0 and self.squares[(x - 1, y - 1)].checker is None:
                                checker.add_jump(self.squares[(x - 1, y - 1)])
                                checker.player.add_killable(self.squares[(x, y)].checker)


    def select_checker(self, x, y):
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
        if self.squares[(x, y)].checker is not None and self.squares[(x, y)].checker.player is self.turn and \
                (not self.turn.must_attack or (self.turn.must_attack and self.squares[(x, y)].checker.jumps)):
            self.selected_checker = self.squares[(x, y)].checker
            if checker.jumps:
                self.select_view_jump_checker(checker)
            else:
                self.select_view_reachable_checker(checker)


    def select_view_reachable_checker(self, checker):
        """
            Color the view selection of reachable adjacent squares (color in blue)
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

        for square in self.selected_checker.reachable_squares:
            self.view.color_object(square.ui, "#0000FF")


    def select_view_jump_checker(self, checker):
        """
            Color the view selection of jumps (color in blue)
        """

        assert isinstance(
            checker, Checker), "'checker' must be an instance of Checker"

        for square in self.selected_checker.jumps:
            self.view.color_object(square.ui, "#0000FF")


    def handle_canvas_click(self, event):
        """
            Handle the click event on the canvas

            Arguments
            ----------
            event: object
                the click event
        """
        x = event.x // 80
        y = event.y // 80
        if self.selected_checker is None:
            self.select_checker(x, y)
        elif self.squares[(x, y)] in self.selected_checker.jumps:
            self.jump(x, y)
            if self.turn.must_attack != 2:
                # If the piece didn't become a king or no jumps available from same piece
                self.change_turn()
            else:
                self.compute_all_moves()
        elif self.squares[(x, y)] in self.selected_checker.reachable_squares:
            if not self.turn.must_attack:
                self.simple_move(x, y)
                self.change_turn()
            else:
                return
        elif self.turn.must_attack == 2:
            return
        else:
            self.reset_selection()
            self.select_checker(x, y)


    def handle_ai_decision(self, idx_checker, idx_square, move_type):
        self.selected_checker = self.board.turn.checkers[idx_checker]
        if move_type == "jump":
            square = self.selected_checker.jumps[idx_square]
            killed_checker, became_king = self.jump(square.x, square.y)
            if self.turn.must_attack != 2:
                # If the piece didn't become a king or no jumps available from same piece
                self.change_turn()
            else:
                self.compute_all_moves()
        else:
            square = self.selected_checker.reachable_squares[idx_square]
            if not self.turn.must_attack:
                self.simple_move(square.x, square.y)
                self.change_turn()
            else:
                raise Exception("Not supposed to happen")


    def jump(self, x, y):
        """
            Make the jump of a checker

            Arguments
            ----------
            x: int
                The abscissa position to jump
            y: int
                The ordinate position to jump
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        # kill the checker jumped
        if x < self.selected_checker.x and y < self.selected_checker.y:
            killed_x, killed_y = x + 1, y + 1
        elif x < self.selected_checker.x and y > self.selected_checker.y:
            killed_x, killed_y = x + 1, y - 1
        elif x > self.selected_checker.x and y < self.selected_checker.y:
            killed_x, killed_y = x - 1, y + 1
        else:
            killed_x, killed_y = x - 1, y - 1
            
        self.kill_checker(self.squares[killed_x, killed_y].checker)
        self.turn.last_jump_moves = 0

        became_king = self.make_move(x, y)

        if self.view is not None:
            self.reset_view_selection()
            self.update_view_scores()

        # If the checker didn't become a king
        if not became_king:

            self.compute_checker_moves(self.selected_checker)
            if self.selected_checker.jumps:
                self.turn.must_attack = 2

                if self.view is not None:
                    self.select_view_jump_checker(self.selected_checker)
            else:
                self.turn.must_attack = 0
        
        return self.squares[killed_x, killed_y].checker, became_king


    def simple_move(self, x, y):
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

        self.turn.last_jump_moves += 1
        became_king = self.make_move(x, y)
        self.reset_selection()

        return became_king
        

    def change_turn(self):
        """
            Change the player turn
        """
        self.selected_checker = None
        self.turn.time += 1
        self.turn.must_attack = 0

        old_turn  = self.turn
        self.turn = self.players[0] if self.turn is self.players[1] else self.players[1]
        
        encoded_board = self.encode_board()

        if encoded_board in self.encodedBoards:
            self.encodedBoards[encoded_board] += 1
        else:
            self.encodedBoards[encoded_board] = 1

        if not self.turn.checker_nb or self.turn.must_attack == -1:
            self.win(old_turn)

        else:
            if self.encodedBoards[encoded_board] > 2:
                        # A faire
                self.draw(False)

            elif old_turn.last_normal_piece_moved_moves >= 40 and self.turn.last_normal_piece_moved_moves >= 40 and \
                    old_turn.last_jump_moves and self.turn.last_jump_moves >= 40:
                self.draw(True)
    
        self.compute_all_moves()


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

        self.game_state = GameState.WIN_WHITE if player.id == 1 else GameState.WIN_BLACK


    def draw(self, reason):
        """
            Declare it is a draw

            Arguments
            ----------
            reason: boolean
                The reason why it is a draw: False if the board was the same 3 times, True if no piece were killed or normal
                piece was moved for 40 round for each player
        """
        assert type(reason) is bool, "'reason' must be a boolean."

        self.game_state = GameState.DRAW


    def reset_selection(self):
        """
            Reset the selection of a piece
        """

        if self.view is not None:
            self.reset_view_selection()
        self.selected_checker = None


    def reset_view_selection(self):
        """
            Reset the view selection (blue squares back to normal)
        """
        for square in self.selected_checker.reachable_squares:
            self.view.color_object(square.ui, square.color)
        for square in self.selected_checker.jumps:
            self.view.color_object(square.ui, square.color)


    def make_move(self, x, y):
        """
            Move the selected checker to a new position

            Arguments
            ----------
            x: int
                The abscissa position
            y: int
                The ordinate position
        """

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        old_x, old_y = self.selected_checker.x, self.selected_checker.y
        self.selected_checker.x, self.selected_checker.y = x, y

        self.squares[(x, y)].checker = self.selected_checker
        self.squares[(old_x, old_y)].checker = None

        if self.view is not None:
            self.view.move_checker(self.selected_checker.ui, x, y)

        self.turn.last_normal_piece_moved_moves = 0 if self.selected_checker.state is State.NORMAL \
            else self.turn.last_normal_piece_moved_moves + 1

        became_king = False

        if (y == 0 and self.turn is self.players[1] or y == self.length - 1 and self.turn is self.players[0]) and self.selected_checker.state is not State.KING:
            self.change_into_king()
            # When a piece becomes a king, the player can't play again
            became_king = True
        
        return became_king


    def change_into_king(self):
        """
            Change into a king the selected checker
        """
        self.selected_checker.state = State.KING
        self.selected_checker.player.king_nb += 1

        if self.view is not None:
            change_into_king_view(checker)

    def change_into_king_view(self, checker):
        new_ui = self.view.change_into_king(checker.ui, checker.x, checker.y, checker.color)
        checker.ui = new_ui

    def kill_checker(self, checker):
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

        if self.view is not None:
            self.view.kill_checker(checker.ui)


    def update_view_scores(self):
        self.view.update_scores(self.players[1].checker_nb, self.players[0].checker_nb)

    def __deepcopy__(self, memodict={}):
        new_board = Board("copy")
        new_board.view = None
        new_board.players  = []

        new_board.selected_checker = None
        new_board.game_state       = copy.copy(game_state)
        new_board.encodedBoards    = copy.copy(encodedBoards)

        for player in self.players:
            new_player += Player(player.name, player.id)
            new_player.time        = player.time
            new_player.ai          = player.ai
            new_player.checker_nb  = player.checker_nb
            new_player.must_attack = player.must_attack
            new_player.checkers    = []
            new_player.last_jump_moves = player.last_jump_moves
            new_player.last_normal_piece_moved_moves = player.last_normal_piece_moved_moves
            
            new_board.players += new_player    

        new_board.turn = new_board.players[0] if self.turn.id == 0 else new_board.players[1]   
        
        new_board.squares  = {}
        for square in self.squares:
            new_squares[(x, y)] = Square(x, y)

        new_board.checkers = []
        for checker in self.checkers:
            new_checker = Checker(checker.x, checker.y, new_board.players[0] if checker.player.id == 0 else new_board.players[1], checker.id)
            new_checker.state = checker.state
            new_checker.color = checker.color
            if new_checker.state != State.DEAD:
                new_squares[(checker.x, checker.y)].checker = new_checker
            new_checker.player.checkers += new_checker
        
        return new_board
            

        