from Board import Board

class Environment():

    def __init__(self, board, training):
        self.board    = board
        self.training = training


    def reset(self):
        self.board.init()
        self.retrieve_all_actions()
        return self.board.encode_board_np(), self.actions
    
    #actions[checker, idx_list_jump_or_move]
    def step(self, idx_action):
        idx_checker, idx_jump, move_type, value_board, board = self.actions[idx_action]
        self.board.handle_ai_decision(idx_checker, idx_jump, move_type)

        if not self.training:
            return

        reward = self._compute_reward(board)
        best_reward = np.max([self._compute_reward(action[4]) for action in self.actions])
        self.retrieve_all_actions()

        return self.board.encode_board_np(), self.actions, reward, best_reward

    def retrieve_all_actions(self):
        self.actions = []

        if self.board.turn.must_attack == 1:
            for idx_checker, checker in enumerate(self.board.turn.checkers):
                for idx_jump, jump in checker.jumps:
                    board = copy.deepcopy(self.board)
                    board.handle_ai_decision(idx_checker, idx_jump, "jump")
                    self.actions += [(idx_checker, idx_jump, "jump", _get_board_state(board), board)]

        elif self.board.turn.must_attack == 2:
            for idx_checker, checker in enumerate(self.board.turn.checkers):
                if checker is self.board.selected_checker:
                    for idx_jump, jump in enumerate(board.selected_checker):
                        board = copy.deepcopy(board)
                        board.handle_ai_decision(idx_checker, idx_jump, "jump")
                        self.actions += [(idx_checker, idx_jump, "jump", _get_board_state(board), board)]
                    break

        else:
            for idx_checker, checker in enumerate(self.board.turn.checkers):
                for idx_move, move in enumerate(checker.reachable_squares):
                    board = copy.deepcopy(board)
                    board.handle_ai_decision(idx_checker, idx_jump, "move")
                    self.actions += [(idx_checker, idx_jump, "move", _get_board_state(board), board)]
                
    def _get_board_state(self, board):
        permute = board.turn is board.players[0]
        state   = board.encode_board_np()

        if permute:
            state = -state.T

        return state
    

    def _compute_reward(self, action):
        if action.game_state is WIN_WHITE and self.board.turn.id == 1 or\
            action.game_state is WIN_BLACK and self.board.turn.id == 0:
            return 100
        elif action.game_state is WIN_WHITE and self.board.turn.id == 0 or\
            action.game_state is WIN_BLACK and self.board.turn.id == 1:
            return -100
        elif action.game_state is Draw:
            return 0

        player_id   = self.board.turn.id
        opponent_id = 1 - player_id
        vulnerable_normal_checkers = action.players[opponent_id].killable_normals / (action.players[player_id].checker_nb - action.players[player_id].king_nb)
        vulnerable_king_checkers   = action.players[opponent_id].killable_kings / action.players[player_id].king_nb
        killable_normal_checkers   = action.players[player_id].killable_normals / (action.players[opponent_id].checker_nb - action.players[opponent_id].king_nb)
        killable_king_checkers     = action.players[player_id].killable_kings / action.players[opponent_id].king_nb

        opponent_king_nb    = action.players[opponent_id].king_nb
        opponent_checker_nb = action.players[opponent_id].checker_nb

        player_king_nb    = action.players[player_id].king_nb
        player_checker_nb = action.players[player_id].checker_nb
        
        reward = - vulnerable_normal_checkers - 2 * vulnerable_king_checkers +\
                 killable_normal_checkers + 2 * killable_king_checkers +\
                 2 * (player_king_nb - opponent_king_nb) / (player_king_nb + opponent_king_nb) +\
                 (player_checker_nb - opponent_checker_nb) / (player_checker_nb + opponent_checker_nb)

        return reward