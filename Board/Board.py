
class Board:
    rows = 6
    columns = 7

    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

    # columns go from 1 to 7 here, hence the "column - 1"
    def add_chip(self, player, column):
        empty_row = self.get_top_column(column - 1)
        if empty_row != -1:
            self.set_board_position(empty_row, column - 1, player)

    def set_board_position(self, row, column, player):
        self.board[row][column] = player

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def get_top_column(self, column):
        current_row = 0
        while self.board[current_row][column] == 0:
            current_row += 1
            if current_row == 6:
                break
        return current_row - 1

    def get_board_position(self, row, column):
        return self.board[row][column]

    def get_diagonal_start(self, row, column):
        while column != 0 and row != 5:
            column -= 1
            row += 1
        return [row, column]

    def get_anti_diagonal_start(self, row, column):
        while column != 0 and row != 0:
            column -= 1
            row -= 1
        return [row, column]

    def is_possible_move(self, row, column):
        if row == self.get_top_column(column):
            return True
        return False
