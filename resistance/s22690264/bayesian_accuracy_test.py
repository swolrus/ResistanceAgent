import matplotlib.pyplot as plt
from random import seed, randrange
from game import Game, Round
from datetime import datetime
from agent import Agent
import s22690264.common.util as util
from s22690264.belief_states import Belief
from s22690264.bots.bayesian import BayesianAgent


class Test:
    def __init__(self, agent_counts):
        self.agent_counts = agent_counts
        self.n_players = sum(agent_counts)
        self.agents = util.get_agent_array(self.agent_counts)
        self.b = Belief()
        self.b.calc_states(sum(self.agent_counts), Agent.spy_count[self.n_players])
        self.accuracy = [{i: [0, 0] for i in range(5)} for _ in range(len(self.b.p_states))]
        self.totals = [0] * 5

    def save(self, name, subfolder):
        util.save_obj(self.accuracy, name, subfolder)

    def load(self, name, subfolder):
        self.accuracy = util.load_obj(name, subfolder)

    def simulate(self, n_epoch, n_games_per_epoch, test=False):
        agents_ = self.agents.copy()
        agents_ = util.shuffle_agents(agents_)

        self.accuracy = [{r: [0, 0] for r in range(5)} for _ in range(10)]

        for epoch in range(n_epoch):
            seed(datetime.now())
            print('BATCH ' + str(epoch) + ' SIM')
            leader_id = randrange(self.n_players)
            for play in range(n_games_per_epoch):
                agents_ = util.shuffle_agents(agents_)
                game = Game(agents_)
                leader_id = (leader_id + 1) % self.n_players

                for i in range(5):
                    game.rounds.append(Round(leader_id, game.agents, game.spies, i))
                    if not game.rounds[i].play():
                        game.missions_lost += 1
                    leader_id = (leader_id + len(game.rounds[i].missions)) % self.n_players
                    for a in game.agents:
                        a.round_outcome(i + 1, game.missions_lost)

                        if a.player_number not in game.spies and isinstance(a, BayesianAgent):
                            true_state = tuple(1 if i in game.spies else 0 for i in range(self.n_players))
                            rank = a.get_correct_rank(true_state)
                            if test is False:
                                for j in range(10):
                                    if j == rank:
                                        self.accuracy[j][i][0] += 1
                                        self.totals[i] += 1
                                    self.accuracy[j][i][1] += 1
                            else:
                                s = 'Round {} try {} was matched at {}'.format(str(a.n_round), str(a.n_try), str(rank))
                                print(s)
                for a in game.agents:
                    a.game_outcome(game.missions_lost > 2, game.spies)

    def plot(self):
        percents = [[(i[0] / i[1]) * 100 if i[1] > 0 else 0 for i in r.values()] for r in self.accuracy]
        X = list(range(1, 6))
        rticks = ['R' + util.get_sub(str(i + 1)) + '(' + str(self.totals[i]) + ')' for i in range(5)]
        gticks = ['G' + util.get_sub(str(i + 1)) for i in range(5)]
        y1 = [percents[0][i] for i in range(5)]
        y2 = [percents[1][i] for i in range(5)]
        y3 = [percents[2][i] for i in range(5)]

        plt.figure(1)
        plt.suptitle('Beyesian Belief Network Guess Accuracy', fontsize=12)

        plt.subplot(121)
        plt.title('Single Guesses')
        plt.plot(X, y1, color=util.COLORS[3], label='1')
        plt.plot(X, y2, color=util.COLORS[1], label='2')
        plt.plot(X, y3, color=util.COLORS[0], label='3')
        plt.xticks(X, rticks, multialignment='center', fontsize=8)
        plt.xlabel('Round (n)', multialignment='center', fontsize=10)
        plt.ylabel('Accuracy (%)', fontsize=10)
        plt.yticks(fontsize=8)
        plt.ylim(0, 100)
        plt.legend(labels=gticks)

        plt.subplot(122)
        plt.title('Accumulative Guesses')
        y3_bot = [y1[i] + y2[i] for i in range(len(y3))]
        plt.bar(X, y1, color=util.COLORS[3], label='1')
        plt.bar(X, y2, bottom=y1, color=util.COLORS[1], label='2')
        plt.bar(X, y3, bottom=y3_bot, color=util.COLORS[0], label='3')
        plt.xticks(X, rticks, multialignment='center', fontsize=8)
        plt.xlabel('Round (n)', multialignment='center', fontsize=10)
        plt.ylabel('Accuracy (%)', fontsize=10)
        plt.yticks(fontsize=8)
        plt.ylim(0, 100)
        plt.legend(labels=gticks)

        plt.tight_layout()
        plt.show()
