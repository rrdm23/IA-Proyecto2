import copy
from Board.Board import Board
from Agent.Agent import Agent


class AgentActions:

    def __init__(self, agent):
        self.agent = agent
        self.player_number = self.agent.player_number

    def play(self, board, column):
        board.add_chip(self.player_number, column)

    def check_possible_win_space(self, board, column_check):
        player = self.player_number
        row_check = board.get_top_column(column_check - 1)
        print(row_check)
        tmp_board = copy.deepcopy(board)
        self.play(tmp_board, column_check)
        print (board.board[5])

        horizontal_check = self.check_horizontal(tmp_board, row_check, player)
        has_horizontal = len(horizontal_check) == 4 \
            and (column_check - 1) in horizontal_check \
            and board.is_possible_move(row_check, column_check - 1)

        has_vertical = self.check_vertical(tmp_board, column_check - 1, player)

        diagonal_check = self.check_diagonal(tmp_board, row_check, column_check - 1, player)
        has_diagonal = len(diagonal_check) == 4 \
            and (column_check - 1) in diagonal_check \
            and board.is_possible_move(row_check, column_check - 1)

        anti_diagonal_check = self.check_anti_diagonal(tmp_board, row_check, column_check - 1, player)
        has_anti_diagonal = len(diagonal_check) == 4 \
            and column_check - 1 in anti_diagonal_check \
            and board.is_possible_move(row_check, column_check - 1)

        if has_horizontal or has_vertical or has_diagonal or has_anti_diagonal:
            self.play(board, column_check)
            return True

        return False

    def check_horizontal(self, board, row, player):
        current_row = board.board[row]
        current_column = 0
        win_columns = []
        for position in current_row:
            if position == player:
                win_columns += [current_column]
                if len(win_columns) == 4:
                    break
            else:
                win_columns = []
            current_column += 1
        return win_columns

    def check_vertical(self, board, column, player):
        current_row = board.get_top_column(column) + 1
        consecutive_chips = 0
        if current_row <= 2:
            while current_row <= 5:
                if board.get_board_position(current_row, column) == player:
                    consecutive_chips += 1
                    if consecutive_chips == 4:
                        return True
                else:
                    consecutive_chips = 0
                current_row -= 1
        return False

    def check_diagonal(self, board, row, column, player):
        win_positions = []
        if (row >= 3 and column >= 4) or (row <= 2 and column <= 2):
            return win_positions
        else:
            init_position = board.get_diagonal_start(row, column)
            row = init_position[0]
            column = init_position[1]
            while row >= 0 and column <= 6:
                if board.get_board_position(row, column) == player:
                    win_positions += [[row, column]]
                    if len(win_positions) == 4:
                        break
                else:
                    win_positions = []
                row -= 1
                column += 1
            return win_positions

    def check_anti_diagonal(self, board, row, column, player):
        win_positions = []
        if (row >= 3 and column <= 2) or (row <= 2 and column <= 3):
            return win_positions
        else:
            init_position = board.get_anti_diagonal_start(row, column)
            row = init_position[0]
            column = init_position[1]
            while row <= 5 and column <= 6:
                if board.get_board_position(row, column) == player:
                    win_positions += [[row, column]]
                    if len(win_positions) == 4:
                        break
                else:
                    win_positions = []
                row += 1
                column += 1
            return win_positions
