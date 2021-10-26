from game import Game
from agent import Agent


class Statistics():
    def __init__(self, agents):
        self.agents = agents
        self.size = len(agents)
        self.stats = {}
        for i in range(self.size):
            self.stats[str(agents[i])] = {'spy_wins': 0, 'spy': 0, 'res_wins': 0, 'res': 0}

    def __str__(self) -> str:
        for agent, data in self.stats.items():
            agent = str(agent)
            self.stats[agent]['spy_winrate'] = data['spy_wins'] / data['spy']
            self.stats[agent]['resistance_winrate'] = data['res_wins'] / data['res']
            self.stats[agent]['combined_winrate'] = (data['spy_wins'] + data['res_wins']) / (data['spy'] + data['res'])

        # order winrates high to low
        s = self.dict_to_ladder(self.stats, 'resistance_winrate')
        s += self.dict_to_ladder(self.stats, 'spy_winrate')
        s += self.dict_to_ladder(self.stats, 'combined_winrate')
        return s

    def add_game(self, game: Game) -> None:
        for i in range(self.size):
            agent_id = game.agents[i].player_number
            agent = str(game.agents[i])
            if agent_id in game.spies:
                # Agent is spy -> update spy total
                self.stats[agent]['spy'] += 1
                if game.missions_lost > 3:
                    # Spies WON, add to spy wincount
                    self.stats[agent]['spy_wins'] += 1
            else:
                # Agent is resistance -> update res total
                self.stats[agent]['res'] += 1
                if game.missions_lost < 3:
                    # Resistance WON, add to res wincount
                    self.stats[agent]['res_wins'] += 1

    def dict_to_ladder(self, stats, sortby):
        s = '\nAgent ' + sortby + ' leaderboard\n'
        sort = []
        sort = sorted(stats.items(), key=lambda tup: tup[1][sortby], reverse=True)
        i = 1
        for key, value in sort:
            s += str(i) + '. Agent ' + str(key) + ' // ' + '{0:.0f}%'.format(value[sortby] * 100) + '\n'
            i += 1

        return s
