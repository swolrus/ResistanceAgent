from game import Game
from agent import Agent


class Statistics():
    def __init__(self, agents: list[Agent]) -> None:
        self.size = len(agents)
        self.stats = {}
        for i in range(self.size):
            self.stats[agents[i].name] = {'spy_wins': 0, 'spy': 0, 'res_wins': 0, 'res': 0}

    def __str__(self) -> str:
        for name, data in self.stats.items():
            self.stats[name]['spy_winrate'] = data['spy_wins'] / data['spy']
            self.stats[name]['resistance_winrate'] = data['res_wins'] / data['res']
            self.stats[name]['combined_winrate'] = (data['spy_wins'] + data['res_wins']) / (data['spy'] + data['res'])

        # order winrates high to low
        s = self.dict_to_ladder(self.stats, 'resistance_winrate')
        s += self.dict_to_ladder(self.stats, 'spy_winrate')
        s += self.dict_to_ladder(self.stats, 'combined_winrate')
        return s

    def add_game(self, game: Game) -> None:
        for i in range(self.size):
            name = game.agents[i].name
            if game.agents[i].player_number in game.spies:
                # Agent is spy -> update spy total
                self.stats[name]['spy'] += 1
                if game.missions_lost > 3:
                    # Spies WON, add to spy wincount
                    self.stats[name]['spy_wins'] += 1
            else:
                # Agent is resistance -> update res total
                self.stats[name]['res'] += 1
                if game.missions_lost < 3:
                    # Resistance WON, add to res wincount
                    self.stats[name]['res_wins'] += 1

    def dict_to_ladder(self, stats: dict, sortby: str) -> str:
        s = '\nAgent ' + sortby + ' leaderboard\n'
        sort = []
        sort = sorted(stats.items(), key=lambda tup: tup[1][sortby], reverse=True)
        i = 1
        for key, value in sort:
            s += str(i) + '. Agent ' + key + ' // ' + '{0:.0f}%'.format(value[sortby] * 100) + '\n'
            i += 1

        return s
