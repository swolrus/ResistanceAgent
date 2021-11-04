from random import randrange, seed
from game import Game, Round, Mission
from datetime import datetime
from agent import Agent
from s22690264.network.model import Model
import s22690264.common.util as util
from s22690264.network.bayesian_train import BayesianTrainAgent
from s22690264.bots.bayesian import BayesianAgent
from s22690264.belief_states import Belief
from s22690264.network.generator import Generator


class Reward:
    def __init__(self, n_players, name):
        self.name = name
        self.n_players = n_players
        self.agents = []
        for i in range(self.n_players):
            self.agents.append(BayesianTrainAgent('i'))
        self.n_players = len(self.agents)
        self.b = Belief()
        self.b.calc_states(self.n_players, 2)
        self.wins = [[[0, 0] for i in range(len(self.b.p_states))]] * 5
        self.nn = [Model(datetime.now(), (len(self.b.p_states) + self.n_players, (len(self.b.p_states)*2)**2, len(self.b.p_states) * 2))] * 5

    def save(self):
        for i in range(len(self.nn)):
            for j in range(len(self.nn[i].nn)):
                util.save_obj(self.nn[i].nn[j].neurons, self.name + str(i) + str(j))

    def load(self):
        for i in range(len(self.nn)):
            for j in range(len(self.nn[i].nn)):
                self.nn[i].nn[j].neurons = util.load_obj(self.name + str(i) + str(j))

    def simulate(self, n, stop_round, gen=None, test=False):
        print('TRAINING FOR ROUND ' + str(stop_round) + ' ' + str(n) + 'TIMES!')
        for _ in range(n):
            for role in [0, 1]:
                agent_beliefs = []
                for r in range(5):
                    seed(datetime.now())
                    self.saved = False
                    agents_ = self.agents.copy()
                    agents_ = util.shuffle_agents(agents_)
                    game = Game(agents_)
                    leader_id = randrange(self.n_players)
                    i = 0
                    while i < 5:
                        game.rounds.append(Round(leader_id, game.agents, game.spies, i))
                        if not game.rounds[i].play():
                            game.missions_lost += 1
                        leader_id = (leader_id + len(game.rounds[i].missions)) % len(game.agents)
                        if i == stop_round:
                            a = game.agents[randrange(self.n_players)]
                            if role == 1:
                                while a.player_number not in game.spies:
                                    a = game.agents[randrange(self.n_players)]
                            else:
                                while a.player_number in game.spies:
                                    a = game.agents[randrange(self.n_players)]
                            agent_beliefs = [role, a.player_number, a.beliefs.beliefs.values()]
                        i += 1

                    for a in self.agents:
                        a.game_outcome(game.missions_lost > 2, len(game.spies))

                state = tuple([1. if j in game.spies else 0. for j in range(self.n_players)])
                a = game.agents[randrange(self.n_players)]
                index = self.b.p_states.index(state)

                inputs = [1. if i == agent_beliefs[1] else 0. for i in range(self.n_players)]
                inputs.extend(agent_beliefs[2])
                if agent_beliefs[0] == 0:
                    outputs = []
                    for i in range(len(self.b.p_states)):
                        if i == index:
                            outputs.append(0)
                            outputs.append(1)
                        else:
                            outputs.append(1)
                            outputs.append(0)
                    if agent_beliefs[0] == 1:
                        outputs = [0. if i == 1 else 0. for i in outputs]
                if gen is None:
                    self.nn[stop_round].gen.add(inputs, outputs)
                else:
                    gen.add(inputs, outputs)

    def train_net(self, i, n):
        # self.simulate(n, 0)
        # self.nn[0].generator_train(0.02, 2, 4, 2, debug=True)
        self.load()
        gen = Generator()
        self.simulate(50, 0, gen)
        gen.split_data(50)
        rows = next(gen)
        for row in rows:
            output = self.nn[0](row[0])
            probs = []
            true = []
            for i in range(0, len(output) - 1, 2):
                probs.append(output[i] - output[i + 1])
                if row[1][i - 5] == 1:
                    true.append(1)
                else:
                    true.append(0)
            print(row[0])
            print(probs)
            print(true)

        self.save()
