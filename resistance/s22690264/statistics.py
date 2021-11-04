import matplotlib.pyplot as plt
from random import seed
from datetime import datetime
from math import floor
from game import Game
import copy
import s22690264.common.util as util


STAT_KEYS = [['SPY WINRATE PER BATCH', 'spy', True], ['RESISTANCE WINRATE PER BATCH', 'res', False], ['TOTAL WINS PER BATCH', 'total', None]]


class Battle:
    def __init__(self, agent_counts, graph, key=None):
        self.plot_key = key
        self.agent_counts = agent_counts
        self.graph = graph
        self.agents = util.get_agent_array(agent_counts)
        self.batches = []
        self.totals = []

    def run(self, batches, plays, accumulate=True, persist=False, top=10):
        seed(datetime.now())
        self.batches = []
        self.totals = []
        self.agents_ = self.agents.copy()
        self.agents_ = util.shuffle_agents(self.agents_)
        self.globals = Statistics(self.agents)
        self.batch = Statistics(self.agents)
        for batch in range(batches):
            print('BATCH ' + str(batch) + ' SIM')
            self.batch = Statistics(self.agents_)

            # shuffle agents when accumulate is false
            # allows for cross batch testing
            if accumulate is False:
                self.agents_ = self.agents.copy()
                self.agents_ = util.shuffle_agents(self.agents_)

            # only increment i when the correct data has been logged to ensure even values of n
            i = 0
            while i < plays:
                game = Game(self.agents_)
                game.play()
                if (STAT_KEYS[self.plot_key][2] and (game.missions_lost > 2)) or (not STAT_KEYS[self.plot_key][2] and not (game.missions_lost > 2)):
                    self.globals.add_game(game)
                    self.batch.add_game(game)
                    i += 1
            if self.graph is not True:
                print('\n{:~^41}'.format('BATCH ' + str(batch)) + str(self.globals))

            if persist is False:
                self.batches.append(copy.deepcopy(self.batch.stats))
                self.totals.append(copy.deepcopy(self.batch.totals))
            else:
                self.batches.append(copy.deepcopy(self.globals.stats))
                self.totals.append(copy.deepcopy(self.globals.totals))

        if accumulate is True:
            self.batch.top = 10
        if self.graph is not True:
            print('\n{:~^41}'.format('GLOBAL') + str(self.globals))
        if self.plot_key is not None:
            self.plot(STAT_KEYS[self.plot_key][1])

    def get_percents(self, key):
        y = {}
        for agent in self.agents:
            color = util.get_color(agent)
            y[agent.name] = [color, []]
            for i in range(len(self.batches)):
                batch = self.batches[i]
                a = batch[agent.name]
                if key == 'spy':
                    percent = (a['spy_wins'] / self.totals[i]['spy']) * 100
                if key == 'res':
                    percent = (a['res_wins'] / self.totals[i]['res']) * 100
                if key == 'total':
                    percent = (a['spy_wins'] + a['res_wins']) / (self.totals[i]['total'] * 100)
                y[agent.name][1].append(percent)
        return y

    def plot(self, key):
        y = self.get_percents(key)
        X = range(len(self.batches))
        xticks = ['B' + str(i) + '\n(' + str(self.totals[i][key]) + ')' for i in range(len(self.batches))]

        plt.figure(1)
        plt.suptitle(STAT_KEYS[self.plot_key][0], fontsize=12)

        for name, data in y.items():
            plt.plot(X, data[1], color=data[0], label=name, marker='+')

        plt.xticks(X, xticks, multialignment='center', fontsize=8)
        plt.xlabel('Batch (n)', multialignment='center', fontsize=10)
        plt.ylabel('Win (%)', fontsize=10)
        plt.yticks(fontsize=8)

        plt.tight_layout()
        plt.legend()
        plt.show()


class Statistics():
    def __init__(self, agents):
        self.agents = agents
        self.size = len(agents)
        self.full_reset()

    def __str__(self) -> str:
        for agent in self.agents:
            agent = self.stats[agent.name]
            agent['spy_winrate'] = (agent['spy_wins'] / self.totals['spy']) if self.totals['spy'] > 0 else 0
            agent['resistance_winrate'] = agent['res_wins'] / self.totals['res']
            agent['combined_winrate'] = (agent['spy_wins'] + agent['res_wins']) / self.totals['total']

        # order winrates high to low
        s = self.dict_to_ladder(self.stats, self.totals, 'resistance_winrate')
        s += self.dict_to_ladder(self.stats, self.totals, 'spy_winrate')
        s += self.dict_to_ladder(self.stats, self.totals, 'combined_winrate')
        return s

    def floored_percentage(self, val, digits):
        val *= 10 ** (digits + 2)
        return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

    def full_reset(self):
        self.totals = {}
        self.totals['total'] = 0
        self.totals['spy'] = 0
        self.totals['res'] = 0

        self.stats = {}
        for i in range(self.size):
            self.stats[self.agents[i].name] = {'spy_wins': 0, 'res_wins': 0}

    def add_game(self, game):
        for i in range(len(game.agents)):
            if game.agents[i].player_number in game.spies:
                # Agent is spy -> update spy total
                if (game.missions_lost > 2):
                    self.stats[game.agents[i].name]['spy_wins'] += 1
            elif (game.missions_lost < 3):
                self.stats[game.agents[i].name]['res_wins'] += 1
        if (game.missions_lost > 2):
            self.totals['spy'] += 1
        else:
            self.totals['res'] += 1
        self.totals['total'] += 1

    def dict_to_ladder(self, stats, totals, sortby, top=10):
        stats = stats.copy()
        s = ''
        sort = []
        sort = sorted(stats.items(), key=lambda tup: tup[1][sortby], reverse=True)
        i = 1
        for agent, value in sort:
            if i <= top:
                s += '\n' + '| {:<25} | {:>9s} |'.format(str(i) + '. Agent ' + agent, self.floored_percentage(value[sortby], 2))
            i += 1
        v = 'n='
        if sortby == 'resistance_winrate':
            v += str(totals['res'])
        elif sortby == 'spy_winrate':
            v += str(totals['spy'])
        else:
            v += str(totals['total'])
        s = '\n_-=*' + sortby.upper().replace('_', ' ') + '*=-_' + s
        s += '\n'
        return s
