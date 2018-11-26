
class Agent:
    player_number = 0

    def __init__(self, char_1, char_2, char_3, char_4):
        self.char_1 = char_1
        self.char_2 = char_2
        self.char_3 = char_3
        self.char_4 = char_4
        self.victory_number = 0

    def set_char_1(self, char_1):
        self.char_1 = char_1

    def set_char_2(self, char_2):
        self.char_2 = char_2

    def set_char_3(self, char_3):
        self.char_3 = char_3

    def set_char_4(self, char_4):
        self.char_4 = char_4

    def set_player_number(self, player_number):
        self.player_number = player_number

    def inc_victory_number(self):
        self.victory_number += 1

    def clear_victory_number(self):
        self.victory_number = 0

    def get_char_1(self):
        return self.char_1

    def get_char_2(self):
        return self.char_2

    def get_char_3(self):
        return self.char_3

    def get_char_4(self):
        return self.char_4

    def get_victory_number(self):
        return self.victory_number

    def get_player_number(self):
        return self.player_number
