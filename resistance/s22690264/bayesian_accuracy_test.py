import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from random import seed
from game import Game, Round, Mission
from datetime import datetime
from agent import Agent
from s22690264.common import util
from s22690264.belief_states import Belief
from s22690264.bots.bayesian import BayesianAgent


class Test:
    def __init__(self, agents=None):
        if agents is not None:
            self.agents_ = agents.copy()

    def save(self, name, subfolder):
        util.save_obj(self.accuracy, name, subfolder)

    def load(self, name, subfolder):
        self.accuracy = util.load_obj(name, subfolder)

    def plot(self):
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        print(self.accuracy)
        percents = [[(i[0] / i[1]) * 100 for i in j] for j in self.accuracy]
        X = range(1, 6)
        xticks = ['R' + str(i).translate(SUB) + '\n(' + str(self.accuracy[i - 1][0][1]) + ')' for i in range(1, 6)]

        y1 = [i[0] for i in percents]
        y2 = [i[1] for i in percents]
        y3 = [i[2] for i in percents]

        y4 = [sum(i) for i in percents]
        y5 = [sum([i[0], i[1]]) for i in percents]

        plt.figure(1)
        plt.suptitle('Beyesian Belief Network Guess Accuracy', fontsize=12)

        plt.subplot(121)
        plt.plot(X, y1, color=(0, 0, 0, 0.9), label='1', marker='+')
        plt.plot(X, y2, color=(0, 0, 0, 0.6), label='2', marker='+')
        plt.plot(X, y3, color=(0, 0, 0, 0.3), label='3', marker='+')
        plt.xticks(X, xticks, multialignment='center', fontsize=8)
        plt.xlabel('Round (n)', multialignment='center', fontsize=10)
        plt.ylabel('Accuracy (%)', fontsize=10)
        plt.yticks(fontsize=8)
        plt.ylim(0, 100)
        plt.legend(title='Single Guesses')

        plt.subplot(122)
        plt.plot(X, y4, color=(0, 0, 0, 0.9), label='All', marker='+')
        plt.plot(X, y5, color=(0, 0, 0, 0.6), label='1,2', marker='+')
        plt.xticks(X, xticks, multialignment='center', fontsize=8)
        plt.xlabel('Round (n)', multialignment='center', fontsize=10)
        plt.ylabel('Accuracy (%)', fontsize=10)
        plt.yticks(fontsize=8)
        plt.ylim(0, 100)
        plt.legend(title='Combined Guesses')

        plt.tight_layout()
        plt.show()

    def simulate(self, n_epoch, n_games_per_epoch, n_agents=None, test=False):
        if n_agents is None:
            self.agents = self.agents_.copy()
            self.n_agents = len(self.agents)
        else:
            self.n_agents = n_agents
            self.agents = self.new_agents(n_agents)

        self.b = Belief()
        self.b.calc_states(len(self.agents), Agent.spy_count[n_agents])

        self.accuracy = [[[0, 0] for i in range(3)] for r in range(5)]

        for epoch in range(n_epoch):
            seed(datetime.now())
            print('EPOCH ' + str(epoch))
            leader_id = 0
            for play in range(n_games_per_epoch):
                seed(datetime.now())
                agents = self.new_agents(n_agents)
                game = Game(agents)
                leader_id = (leader_id + 1) % n_agents

                for i in range(5):
                    game.rounds.append(Round(leader_id, game.agents, game.spies, i))
                    if not self.play_round(game.rounds[i], game, test):
                        game.missions_lost += 1
                    leader_id = (leader_id + len(game.rounds[i].missions)) % n_agents
                    for a in game.agents:
                        a.round_outcome(i + 1, game.missions_lost)
                    if game.missions_lost > 2:
                        break
                for a in game.agents:
                    a.game_outcome(game.missions_lost > 2, game.spies)

    def play_round(self, rnd, game, test):
        mission_size = Agent.mission_sizes[len(rnd.agents)][rnd.rnd]
        fails_required = Agent.fails_required[len(rnd.agents)][rnd.rnd]
        while len(rnd.missions) < 5:
            team = rnd.agents[rnd.leader_id].propose_mission(mission_size, fails_required)
            mission = Mission(rnd.leader_id, team, rnd.agents,
                          rnd.spies, rnd.rnd, len(rnd.missions) == 4)
            for a in rnd.agents:
                if a.player_number not in game.spies and isinstance(a, BayesianAgent):
                    true_state = tuple(1 if i in game.spies else 0 for i in range(self.n_agents))
                    rank = a.get_correct_rank(true_state)
                    if test is False:
                        for i in range(3):
                            if i == rank:
                                self.accuracy[rnd.rnd][i][0] += 1
                            self.accuracy[rnd.rnd][i][1] += 1
                    else:
                        s = 'Round{' + str(a.n_round) + '}'
                        s += ' Try{' + str(a.n_try) + '}\n'
                        s += 'was matched at ' + str(rank) + '\n'
                        print(s)

            rnd.missions.append(mission)
            rnd.leader_id = (rnd.leader_id + 1) % len(rnd.agents)
            if mission.is_approved():
                return mission.is_successful()
        return mission.is_successful()

    def set_agents(self, agents):
        self.agents_ = agents.copy()

    def new_agents(self, size):
        return [BayesianAgent(i) for i in range(size)]
