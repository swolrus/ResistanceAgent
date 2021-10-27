from game import Game
from s22690264.bots.random import RandomAgent
from s22690264.bots.basic import BasicAgent
from s22690264.bots.learn import LearnAgent
from s22690264.statistics import Sim
from s22690264.network.model import Model
from s22690264.network.generator import Generator

agents = [
    LearnAgent('L1'),
    LearnAgent('L2'),
    BasicAgent('b2'),
    BasicAgent('b1'),
    RandomAgent('R1'),
    RandomAgent('R2')
]


def run_sim():
    sim = Sim(agents)
    sim.run(100)
    print(sim)


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
    network = Model(1, (n_inputs, 3, 2, n_outputs), (None, None, 'RelU'))
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
    for i in range(len(dataX)-1):
        print(i)
        gen.add(dataX[i], dataY[i])
    n_inputs = 3
    n_outputs = 2
    network = Model(1, (n_inputs, 3, 2, n_outputs))
    network.generator_train(gen, 0.2, 10, True, 0.9, True)
    print(network)
    print(network.predict([0, 1, 1]))


run_sim()
