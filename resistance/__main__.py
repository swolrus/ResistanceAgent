from random_agent import RandomAgent
from s22690264.basic_agent import BasicAgent
from s22690264.statistics import Statistics
from game import Game


agents = [
    BasicAgent(name='b1'),
    BasicAgent(name='b2'),
    BasicAgent(name='b3'),
    RandomAgent(name='r4'),
    RandomAgent(name='r5'),
    RandomAgent(name='r6'),
    RandomAgent(name='r7')
]

stats = Statistics(agents)

for i in range(1000):
    game = Game(agents)
    game.play()
    # print(game)
    stats.add_game(game)

print(stats)
