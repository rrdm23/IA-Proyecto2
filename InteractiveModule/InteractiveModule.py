import sys
import time
from ../Game.Game import Game
from ../Agent.Agent import Agent


class InteractiveModule:
    def __init__(self):
        self.game = None
        self.args = [0]

    def start_game_auto(self):
        self.game = Game(self.args[0], self.args[1])


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
if not sys.argv[2]:
    sys.argv[2] = ""
main.get_arguments(sys.argv[1], sys.argv[2])
main.start_game()
