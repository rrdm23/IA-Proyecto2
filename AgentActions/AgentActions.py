import copy
import random as rnd
from Board.Board import Board
from Agent.Agent import Agent


class AgentActions:

    def __init__(self, agent):
        self.agent = agent
        self.player_number = self.agent.player_number
        self.has_options = 0

    def play(self, board, column):
        board.add_chip(self.player_number, column)

    def execute_turn(self, board):
        about_to_end = self.check_end_game(board)
        # print(about_to_end)
        column_range = []
        turn_executed = 0
        if about_to_end == "Blocked opponent":
            turn_executed += 1
        elif about_to_end == "Winner":
            return True
        else:
            edges_vs_center = self.generic_move_1()
            seq_vs_spaces = self.generic_move_2(board)
            bottom_vs_top = self.generic_move_3(board)
            over_vs_next = self.generic_move_4(board)

            column_range_start = self.column_intersection(edges_vs_center, seq_vs_spaces)
            if not column_range_start:
                if not seq_vs_spaces:
                    column_range_start += edges_vs_center
                elif not edges_vs_center:
                    column_range_start += seq_vs_spaces
                else:
                    rnd_strategy = rnd.randint(1, 2)
                    if rnd_strategy == 1:
                        column_range_start += edges_vs_center
                    else:
                        column_range_start += seq_vs_spaces
            elif len(column_range_start) == 1 and turn_executed == 0:
                final_decision = column_range_start[0] + 1
                if board.is_possible_move_column(final_decision - 1):
                    # print("Column played: ", final_decision)
                    self.play(board, final_decision)
                    turn_executed += 1

            column_range_move_3 = self.column_intersection(column_range_start, bottom_vs_top)
            if not column_range_move_3:
                if not column_range_start:
                    column_range_move_3 += bottom_vs_top
                elif not bottom_vs_top:
                    column_range_move_3 += column_range_start
                else:
                    rnd_strategy = rnd.randint(2, 3)
                    if rnd_strategy == 2:
                        column_range_move_3 += column_range_start
                    else:
                        column_range_move_3 += bottom_vs_top
            elif len(column_range_move_3) == 1 and turn_executed == 0:
                final_decision = column_range_move_3[0] + 1
                if board.is_possible_move_column(final_decision - 1):
                    # print("Column played: ", final_decision)
                    self.play(board, final_decision)
                    turn_executed += 1

            column_range_final = self.column_intersection(column_range_move_3, over_vs_next)
            if not column_range_final:
                if not column_range_move_3:
                    column_range_final += over_vs_next
                elif not over_vs_next:
                    column_range_final += column_range_move_3
                else:
                    rnd_strategy = rnd.randint(3, 4)
                    if rnd_strategy == 3:
                        column_range_final += column_range_move_3
                    else:
                        column_range_final += over_vs_next
            elif len(column_range_final) == 1 and turn_executed == 0:
                final_decision = column_range_final[0] + 1
                if board.is_possible_move_column(final_decision - 1):
                    # print("Column played: ", final_decision)
                    self.play(board, final_decision)
                    turn_executed += 1

            column_range += column_range_final
            if turn_executed == 0:
                if not column_range:
                    column_range = [0, 1, 2, 3, 4, 5, 6]
                rnd_index = rnd.randint(0, len(column_range) - 1)
                final_decision = column_range[rnd_index] + 1
                # print("Decision: ", final_decision)
                # print("Is possible in column?: ", board.is_possible_move_column(final_decision - 1))
                not_possible = 0
                while not board.is_possible_move_column(final_decision - 1):
                    column_range.remove(final_decision - 1)
                    if not column_range:
                        if not_possible == 1:
                            break
                        else:
                            column_range = [0, 1, 2, 3, 4, 5, 6]
                            not_possible += 1
                        column_range.remove(final_decision - 1)
                    rnd_index = rnd.randint(0, len(column_range) - 1)
                    final_decision = column_range[rnd_index] + 1

                if not_possible == 1:
                    self.has_options = 1
                    return False

                # print("Column played: ", final_decision)
                self.play(board, final_decision)
                turn_executed += 1

        # print("Turn finished")
        return False

    def check_end_game(self, board):
        for col in range(1, 8):
            win = self.check_possible_win_space(board, col, self.player_number)
            if win:
                return "Winner"
            else:
                continue

        opponent_player_number = (self.player_number % 2) + 1
        for col in range(1, 8):
            block = self.check_possible_win_space(board, col, opponent_player_number)
            if block:
                return "Blocked opponent"
            else:
                continue
        return "No situation"

    def check_possible_win_space(self, board, column_check, winning_player):
        if not board.is_possible_move_column(column_check - 1):
            return False
        row_check = board.get_top_column(column_check - 1)
        tmp_board = copy.deepcopy(board)
        self.player_number = winning_player
        self.play(tmp_board, column_check)

        horizontal_check = self.check_horizontal(tmp_board, row_check, winning_player)
        has_horizontal = len(horizontal_check) == 4 \
            and (column_check - 1) in horizontal_check \
            and board.is_possible_move(row_check, column_check - 1)

        has_vertical = self.check_vertical(tmp_board, column_check - 1, winning_player)

        diagonal_check = self.check_diagonal(tmp_board, row_check, column_check - 1, winning_player)
        column_in_diagonal = 0
        for element in diagonal_check:
            if element[1] == column_check - 1:
                column_in_diagonal += 1
                break
        has_diagonal = len(diagonal_check) == 4 \
            and column_in_diagonal == 1 \
            and board.is_possible_move(row_check, column_check - 1)

        anti_diagonal_check = self.check_anti_diagonal(tmp_board, row_check, column_check - 1, winning_player)
        column_in_anti_diag = 0
        for element in anti_diagonal_check:
            if element[1] == column_check - 1:
                column_in_anti_diag += 1
                break
        has_anti_diagonal = len(anti_diagonal_check) == 4 \
            and column_in_anti_diag == 1 \
            and board.is_possible_move(row_check, column_check - 1)

        self.player_number = self.agent.player_number

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
                current_row += 1
        return False

    def check_diagonal(self, board, row, column, player):
        win_positions = []
        init_position = board.get_diagonal_start(row, column)
        new_row = init_position[0]
        new_column = init_position[1]
        if (new_row >= 3 and new_column >= 4) or (new_row <= 2 and new_column <= 2):
            return win_positions
        while new_row >= 0 and new_column <= 6:
            if board.get_board_position(new_row, new_column) == player:
                    win_positions += [[new_row, new_column]]
                    if len(win_positions) == 4:
                        break
            else:
                win_positions = []
            new_row -= 1
            new_column += 1
        return win_positions

    def check_anti_diagonal(self, board, row, column, player):
        win_positions = []
        init_position = board.get_anti_diagonal_start(row, column)
        new_row = init_position[0]
        new_column = init_position[1]
        if (new_row >= 3 and new_column <= 2) or (new_row <= 2 and new_column >= 4):
            return win_positions
        while new_row <= 5 and new_column <= 6:
            if board.get_board_position(new_row, new_column) == player:
                win_positions += [[new_row, new_column]]
                if len(win_positions) == 4:
                    break
            else:
                win_positions = []
            new_row += 1
            new_column += 1
        return win_positions

    # center vs. edges
    def generic_move_1(self):
        decided_move = rnd.uniform(0, 1)
        column_range = []
        if decided_move <= self.agent.get_char_1():
            column_range += [2, 3, 4]
        else:
            column_range += [0, 1, 5, 6]
        return column_range

    # sequence vs. spaces
    def generic_move_2(self, board):
        decided_move = rnd.uniform(0, 1)
        column_range = []
        for col in range(0, board.columns):
            row = board.get_top_column(col)
            if row != 5:
                row += 1
            player_chip = board.get_board_position(row, col)
            if decided_move <= self.agent.get_char_2():
                if player_chip == self.agent.player_number:
                        column_range += [col]
                        if col != 6 and board.is_possible_move(row, col + 1):
                            column_range += [col + 1]
                        if col != 0 and board.is_possible_move(row, col - 1):
                            column_range += [col - 1]
            else:
                if player_chip == self.agent.player_number:
                    if col not in [5, 6] \
                            and board.is_possible_move(row, col + 1) \
                            and board.is_possible_move(row, col + 2):
                                column_range += [col + 2]
                                if col != 4 and board.is_possible_move(row, col + 3):
                                        if (col <= 2
                                                and board.get_board_position(row, col + 4) != self.agent.player_number
                                            )\
                                                or col == 3:
                                            column_range += [col + 3]
                    if col not in [0, 1] \
                            and board.is_possible_move(row, col - 1) \
                            and board.is_possible_move(row, col - 2):
                                column_range += [col - 2]
                                if col != 2 and board.is_possible_move(row, col - 3):
                                    if (col >= 4
                                            and board.get_board_position(row, col - 4) != self.agent.player_number
                                        )\
                                            or col == 3:
                                        column_range += [col - 3]
        return column_range

    # top vs. bottom
    def generic_move_3(self, board):
        decided_move = rnd.uniform(0, 1)
        column_range = []
        if decided_move <= self.agent.get_char_3():
            top_spaces = board.top_board_spaces()
            column_range += top_spaces
        else:
            bottom_spaces = board.bottom_board_spaces()
            column_range += bottom_spaces
        return column_range

    # over vs. next to
    def generic_move_4(self, board):
        decided_move = rnd.uniform(0, 1)
        column_range = []
        for col in range(0, board.columns):
            row = board.get_top_column(col)
            if row == 5:
                continue
            top_chip = board.get_board_position(row + 1, col)
            if top_chip != self.agent.player_number:
                if decided_move <= self.agent.get_char_4():
                    column_range += [col]
                else:
                    if col != 0 and board.is_possible_move(row + 1, col - 1):
                        if (col - 1) not in column_range:
                            column_range += [col - 1]
                    if col != 6 and board.is_possible_move(row + 1, col + 1):
                        if (col + 1) not in column_range:
                            column_range += [col + 1]
        return column_range

    def column_intersection(self, col_list_1, col_list_2):
        temp = set(col_list_2)
        intersection = [value for value in col_list_1 if value in temp]
        return intersection

