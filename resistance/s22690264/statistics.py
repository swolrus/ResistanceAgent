from math import floor
from random import seed
from datetime import datetime
from game import Game


class Tourn:
    def __init__(self, agents):
        self.agents = agents.copy()
        self.globals = Statistics(self.agents)
        self.batch = Statistics(self.agents)

    def run(self, batches, plays, top=10):
        self.batch.top = top
        for batch in range(batches):
            agents = self.agents.copy()
            seed(datetime.now())

            for play in range(plays):
                seed(datetime.now())
                game = Game(agents)
                game.play()
                self.globals.add_game(game)
                self.batch.add_game(game)
            print("BATCH // " + str(batch))
            print(self.batch)
            self.reset()

        self.batch.top = 10
        print(self.globals)
        self.globals.reset(self.agents)

    def reset(self):
        for agent in self.agents:
            agent.reset()


class Statistics():
    def __init__(self, agents):
        self.agents = agents
        self.size = len(agents)
        self.stats = {}
        for i in range(self.size):
            self.stats[agents[i].name] = {'spy_wins': 0, 'spy_plays': 0, 'res_wins': 0, 'res_plays': 0}
        self.total_games, self.spy_wins, self.res_wins = 0, 0, 0
        self.top = 10

    def __str__(self) -> str:
        for agent in self.agents:
            agent = self.stats[agent.name]
            agent['spy_winrate'] = agent['spy_wins'] / self.spy_wins
            agent['resistance_winrate'] = agent['res_wins'] / self.res_wins
            agent['combined_winrate'] = (agent['spy_wins'] + agent['res_wins']) / self.total_games

        # order winrates high to low
        s = self.dict_to_ladder(self.stats, 'resistance_winrate', self.top)
        s += self.dict_to_ladder(self.stats, 'spy_winrate', self.top)
        s += self.dict_to_ladder(self.stats, 'combined_winrate', self.top)
        return s

    def floored_percentage(self, val, digits):
        val *= 10 ** (digits + 2)
        return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

    def reset(self, agents):
        self.agents = agents
        self.stats = {}
        self.total_games = 0
        for i in range(self.size):
            self.stats[agents[i].name] = {'spy_wins': 0, 'spy_plays': 0, 'res_wins': 0, 'res_plays': 0}
        self.total_games, self.spy_wins, self.res_wins = 0, 0, 0

    def add_game(self, game):
        for i in range(len(game.agents)):
            if game.agents[i].player_number in game.spies:
                # Agent is spy -> update spy total
                if (game.missions_lost > 2):
                    self.stats[game.agents[i].name]['spy_wins'] += 1
            elif (game.missions_lost < 3):
                self.stats[game.agents[i].name]['res_wins'] += 1
        if (game.missions_lost >= 3):
            self.spy_wins += 1
        else:
            self.res_wins += 1
        self.total_games += 1

    def dict_to_ladder(self, stats, sortby, top):
        s = '\nAgent ' + sortby + ' leaderboard\n'
        sort = []
        sort = sorted(stats.items(), key=lambda tup: tup[1][sortby], reverse=True)
        i = 1
        for agent, value in sort:
            if i <= top:
                s += str(i) + '. Agent ' + agent + ' // ' + '{}'.format(self.floored_percentage(value[sortby], 2)) + '\n'
            i += 1

        return s
