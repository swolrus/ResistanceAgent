from random import randrange, seed
from game import Game, Round, Mission
from datetime import datetime
from agent import Agent
from s22690264.belief_states import Belief
from .bayesian_train import BayesianTrainAgent
from s22690264.network.model import Model


class Simulate:
    def __init__(self):
        self.agents = self.new_agents()
        self.n_players = len(self.agents)
        self.b = Belief()
        self.nn = None
        self.b.calc_states(self.n_players, 2)
        self.nn = [Model(datetime.now(), (self.n_players, 12, 12, self.n_players))] * 5

    def save(self, name):
        for i in range(len(self.nn)):
            self.nn[i].save_model(str(i), name)

    def load(self, name):
        for i in range(len(self.nn)):
            self.nn[i].load_model(str(i), name)

    def simulate(self, n_epoch, n_games_per_epoch, test=False):
        for epoch in range(n_epoch):
            seed(datetime.now())
            print('EPOCH ' + str(epoch))

            for play in range(n_games_per_epoch):
                self.saved = False
                seed(datetime.now())
                game = Game(self.agents)
                output = [1 if a.player_number in game.spies else 0 for a in game.agents]
                leader_id = 0
                stop = randrange(5)
                for i in range(0, stop):
                    game.rounds.append(Round(leader_id, game.agents, game.spies, i))
                    if not self.play_round(game.rounds[i], game, test, stop, output):
                        game.missions_lost += 1
                    leader_id = (leader_id + len(game.rounds[i].missions)) % len(game.agents)

                a = game.agents[randrange(self.n_players)]
                while a in game.spies:
                    a = game.agents[randrange(self.n_players)]
                inputs = []
                for i in range(len(game.agents)):
                    inputs.append(a.stats[game.agents[i].player_number])
                if test is False:
                    self.round_train(stop, inputs, output)
                else:
                    s = 'Round{' + str(a.n_round) + '}'
                    s += ' Try{' + str(a.n_try) + '}\n'
                    s += 'Input //' + str(inputs) + '\n'
                    s += 'Expected //' + str(output) + '\n'
                    s += 'Got // ' + str(self.nn[stop].predict(inputs)) + '\n'
                    print(s)

    def play_round(self, rnd, game, test, stop, output):
        mission_size = Agent.mission_sizes[len(rnd.agents)][rnd.rnd]
        fails_required = Agent.fails_required[len(rnd.agents)][rnd.rnd]
        while len(rnd.missions) < randrange(1, 5):
            team = rnd.agents[rnd.leader_id].propose_mission(
                mission_size, fails_required)
            mission = Mission(rnd.leader_id, team, rnd.agents,
                              rnd.spies, rnd.rnd, len(rnd.missions) == 4)
            rnd.missions.append(mission)
            rnd.leader_id = (rnd.leader_id + 1) % len(rnd.agents)
            if mission.is_approved():
                return mission.is_successful()
        return mission.is_successful()

    def train_nets(self):
        for i in range(len(self.nn)):
            print('Training network for round ' + str(i))
            print(self.nn[i].gen)

            self.nn[i].generator_train(0.1, 10, batch_size=2000, anneal=True, anneal_rate=0.99, debug=False)

    def round_train(self, index, inputs, output):
        self.nn[index].gen.add(inputs, output)

    def new_agents(self):
        agents = [
            BayesianTrainAgent('r1'),
            BayesianTrainAgent('r2'),
            BayesianTrainAgent('r3'),
            BayesianTrainAgent('r4'),
            BayesianTrainAgent('r5'),
        ]
        return agents
