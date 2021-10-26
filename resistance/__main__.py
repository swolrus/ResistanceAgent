from game import Game
from s22690264.bots.random import RandomAgent
from s22690264.bots.basic import BasicAgent
from s22690264.bots.learn import LearnAgent
from s22690264.statistics import Statistics
from s22690264.network.model import Model
from s22690264.network.generator import Generator

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
    game = Game(agents)
    stats = Statistics(game.agents)
    for i in range(10):
        game = Game(agents)
        game.play()
        # print(game)
        stats.add_game(game)
    agents[3].train()
    print(stats)


def run_game():
    game = Game(agents)
    game.play()


def test_NN():
    dataset = [[0, 1, 0, 1],
               [1, 1, 0, 1],
               [1, 0, 1, 0],
               [1, 1, 1, 1]]

    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set([row[-1] for row in dataset]))
    network = Model(1, (n_inputs, 3, 2, n_outputs))
    network.train(dataset, 0.2, 50, n_outputs, True, True)
    print(network)
    print(network.predict([0, 1, 1]))


def test_NN2():
    dataX = [[0, 1, 0],
             [1, 1, 0],
             [1, 0, 1],
             [1, 1, 1]]
    dataY = [[0, 1], [0, 1], [1, 0], [0, 1]]
    gen = Generator(4)
    for i in range(len(dataX) - 1):
        print(i)
        gen.add(dataX[i], dataY[i])
    n_inputs = 3
    n_outputs = 2
    network = Model(1, (n_inputs, 3, 2, n_outputs))
    network.generator_train(gen, 0.5, 20, True, 0.99, True)
    print(network)
    print(network.predict([0, 1, 1]))


run_sim()
