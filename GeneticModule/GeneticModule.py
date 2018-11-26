import random as rnd
import operator as op
from Agent.Agent import Agent
from AgentActions.AgentActions import AgentActions


class GeneticModule:
    def __init__(self, gen_number, population_number, next_gen_agents):
        self.gen_number = gen_number
        self.population_number = population_number
        self.next_gen_agents = next_gen_agents
        self.actual_agents = []

    def init_population(self):
        population = self.get_population_number()
        while population > 0:
            agent = Agent(
                rnd.uniform(0, 1),
                rnd.uniform(0, 1),
                rnd.uniform(0, 1),
                rnd.uniform(0, 1)
            )
            self.actual_agents += [agent]
            population -= 1

    def fitness_function(self):
        best_agents_list = []
        next_agents_number = self.get_next_gen_agents()
        self.actual_agents.sort(key=op.attrgetter('victory_number'), reverse=True)
        while next_agents_number > 0:
            best_agent = self.actual_agents.pop(0)
            best_agents_list += [best_agent]
        return best_agents_list

    def mutate_agent(self, agent):
        mutation_prob = 0.1
        rand_chance = rnd.uniform(0, 1)
        if rand_chance <= mutation_prob:
            mutation_char = rnd.randint(0, 3)
            switcher = {
                0: agent.set_char_1,
                1: agent.set_char_2,
                2: agent.set_char_3,
                3: agent.set_char_4
            }
            set_char = switcher.get(mutation_char)
            set_char(rnd.uniform(0, 1))

    def crossover(self):
        best_agents = self.fitness_function()
        new_generation = []
        while best_agents:
            parent_agent_1 = best_agents.pop(0)
            parent_agent_2 = best_agents.pop(0)
            child_agent = Agent(
                parent_agent_1.get_char_1(),
                parent_agent_2.get_char_2(),
                parent_agent_1.get_char_3(),
                parent_agent_2.get_char_4()
            )
            child_agent.clear_victory_number()
            self.mutate_agent(child_agent)
            new_generation += [child_agent]
        self.set_actual_agents(new_generation)
        self.set_population_number(len(self.actual_agents))

    def set_gen_number(self, gen_number):
        self.gen_number = gen_number

    def set_population_number(self, population_number):
        self.population_number = population_number

    def set_next_gen_agents(self, next_gen_agents):
        self.next_gen_agents = next_gen_agents

    def set_actual_agents(self, actual_agents):
        self.actual_agents = actual_agents

    def get_gen_number(self):
        return self.gen_number

    def get_population_number(self):
        return self.population_number

    def get_next_gen_agents(self):
        return self.next_gen_agents

    def get_actual_agents(self):
        return self.actual_agents
