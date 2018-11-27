import sys
import time
from GeneticModule.GeneticModule import GeneticModule


class MainGenetics:
    def __init__(self):
        self.args = [0]
        self.gm = None

    def init_genetic_module(self):
        self.gm = GeneticModule(self.args[1], self.args[2], self.args[3])
        time.sleep(1)
        print("Population created with " + str(self.args[2]) + " individuals")
        print("Generations to create: " + str(self.args[1]))
        print("Percentage of individuals to keep in each new generation: " + str(self.args[3]) + "%")
        time.sleep(2)
        print("Preparing to initiate crossovers and generate offspring...")
        time.sleep(1)
        best_agent = self.gm.get_best_offspring()
        print("Copy the info of the agent below, and paste it in the interactive program: ")
        print(best_agent)
        time.sleep(1)
        print("Program finished.")

    def get_arguments(self, gen_number, pop_number, next_gen_agents):
        args = []
        real_gen_number = eval(gen_number[13:])
        real_pop_number = eval(pop_number[13:])
        real_next_agents = eval(next_gen_agents[18:])
        args += [real_gen_number, real_pop_number, real_next_agents]
        self.args += args


main = MainGenetics()
main.get_arguments(sys.argv[1], sys.argv[2], sys.argv[3])
main.init_genetic_module()
