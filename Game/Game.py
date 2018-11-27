from Agent.Agent import Agent
from AgentActions.AgentActions import AgentActions
from Board.Board import Board


class Game:
    turn = 1
    is_winner = False

    def __init__(self, player_1, player_2):
        self.game_board = Board()

        self.player_1_properties = player_1
        self.player_1_properties.set_player_number(1)
        self.player_1 = AgentActions(self.player_1_properties)

        self.player_2_properties = player_2
        self.player_2_properties.set_player_number(2)
        self.player_2 = AgentActions(self.player_2_properties)

    def game_over(self):
        if not self.is_winner:
            return False
        for column in range(0, 7):
            if self.game_board.is_possible_move_column(column):
                return False
        return True

    def continue_match(self):
        if self.turn == 1:
            last_move = self.player_1.execute_turn(self.game_board)
            if last_move:
                self.is_winner = True
                self.player_1.agent.inc_victory_number()
        else:
            last_move = self.player_2.execute_turn(self.game_board)
            if last_move:
                self.is_winner = True
                self.player_2.agent.inc_victory_number()
        self.next_turn()

    def next_turn(self):
        self.turn = (self.turn % 2) + 1

