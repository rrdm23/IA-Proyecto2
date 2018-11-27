import sys
import time
from Board.Board import Board
from Game.Game import Game
from Agent.Agent import Agent
from AgentActions.AgentActions import AgentActions


class InteractiveModule:
    def __init__(self):
        self.game = None
        self.args = []

    def start_game_auto(self):
        print("Match between two agents")
        self.game = Game(self.args[0], self.args[1])

        self.game.player_1.agent.set_player_number(1)
        self.game.player_2.agent.set_player_number(2)

        while not self.game.game_over():
            for row in self.game.game_board.board:
                print(row)
            print("Agent " + str(self.game.turn) + "'s turn. Please wait...")
            time.sleep(3)
            self.game.continue_match()

    def game_over_player(self, board):
        for column in range(0, 7):
            if board.is_possible_move_column(column):
                return False
        return True

    def start_game_player(self):
        winner = 0
        playing_agent = self.args[0]
        playing_agent.set_player_number(2)
        playing_agent_actions = AgentActions(playing_agent)
        print("Match against an agent")
        time.sleep(2)
        board = Board()
        for row in board.board:
            print(row)
        time.sleep(1)
        while winner == 0 and not self.game_over_player(board) and playing_agent_actions.has_options == 0:
            print("Your turn. Pick a number from 1 to 7: ")
            chosen_column = input()
            while chosen_column < 1 or chosen_column > 7:
                print("Error. Pick a correct number (1 to 7): ")
                chosen_column = input()
            board.add_chip(1, chosen_column)

            row_check = board.get_top_column(int(chosen_column) - 2)
            horizontal_check = playing_agent_actions.check_horizontal(board, row_check, 1)
            vertical_check = playing_agent_actions.check_vertical(board, int(chosen_column) - 2, 1)
            diagonal_check = playing_agent_actions.check_diagonal(board, row_check, int(chosen_column) - 2, 1)
            anti_diagonal_check = playing_agent_actions.check_anti_diagonal(board, row_check, int(chosen_column) - 2, 1)

            if len(horizontal_check) == 4 \
                    or vertical_check \
                    or len(diagonal_check) == 4 \
                    or len(anti_diagonal_check) == 4:
                winner += 1

            time.sleep(2)
            for row in board.board:
                print(row)
            print("Agent's turn. Please wait...")
            time.sleep(0)

            agent_turn = playing_agent_actions.execute_turn(board)
            if agent_turn:
                winner += 2

            time.sleep(2)
            for row in board.board:
                print(row)
        print("The winner is player " + str(winner) + "!")

    def get_argument(self, agent):
        args = []
        str_agent = agent[11:]
        param_agent = str_agent.split(",")
        real_agent_values = []
        for value in param_agent:
            real_agent_values += [eval(value)]
        real_agent = Agent(real_agent_values[0], real_agent_values[1], real_agent_values[2], real_agent_values[3])
        args += [real_agent]
        self.args += args


main = InteractiveModule()
param_1 = sys.argv[1]
main.get_argument(param_1)

try:
    param_2 = sys.argv[2]
    main.get_argument(param_2)
    main.start_game_auto()
except IndexError:
    main.start_game_player()

