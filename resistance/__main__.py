from game import Game
from s22690264.bots.random import RandomAgent
from s22690264.bots.basic import BasicAgent
from s22690264.bots.learn import LearnAgent
from s22690264.statistics import Statistics
from s22690264.network.nn import NN

agents = [
    BasicAgent('b1'),
    BasicAgent('b2'),
    BasicAgent('b3'),
    LearnAgent('l4'),
    RandomAgent('r5'),
    RandomAgent('r6'),
    RandomAgent('r7'),
]


def run_sim():
    stats = Statistics(agents)
    for i in range(10000):
        game = Game(agents)
        game.play()
        # print(game)
        stats.add_game(game)
    print(stats)


def run_game():
    game = Game(agents)
    game.play()
    print(game)

def test_NN():
    dataset = [[0, 1, 0, 1],
               [1, 1, 0, 1],
               [1, 0, 1, 0],
               [1, 1, 1, 1]]
    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set([row[-1] for row in dataset]))
    network = NN(1, n_inputs, [3, 2], n_outputs)
    network.train_network(dataset, 0.1, 200, n_outputs)
    print(network)
    print(network.predict([0,1,1,None]))

test_NN()
