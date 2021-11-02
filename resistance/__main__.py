from random import seed
from datetime import datetime
from game import Game
from s22690264.network.model import Model
from s22690264.bots.random import RandomAgent
from s22690264.bots.basic import BasicAgent
from s22690264.bots.basic_learn import BasicLearnAgent
from s22690264.bots.bayesian import BayesianAgent
from s22690264.network.data import Simulate
from s22690264.bayesian_accuracy_test import Test

agents = [
    BayesianAgent('Bayesian2'),
    BasicAgent('Based1'),
    BasicAgent('Based2'),
    BasicAgent('Based3'),
    BasicAgent('Based4'),
]


def run_sim():
    tournament = Simulate(agents)
    tournament.run(2, 10)


def run_game():
    seed(datetime.now())
    game = Game(agents_two)
    game.play()
    print(game.spies)


def test():
    test = Test(agents)
    test.simulate(100, 100, 5)
    test.save('test2', 'accuracy')

    test2 = Test()
    test2.load('test2', 'accuracy')
    test2.plot()


def test2():
    nn = Model(5)
    nn.add_hidden_layer(2, 'ReLu')
    nn.close_network(2, 'sigmoid')
    nn.gen.add([0, 1, 1, 0, 1], [1, 0])
    nn.gen.add([1, 1, 0, 1, 1], [1, 0])
    nn.gen.add([1, 0, 1, 0, 0], [0, 1])
    nn.gen.add([0, 0, 0, 1, 1], [0, 1])
    nn.gen.add([0, 1, 1, 1, 0], [1, 0])
    nn.gen.add([1, 1, 0, 0, 1], [1, 0])
    nn.generator_train(1q, 1)
    results = []
    results.append(nn([1, 0, 1, 0, 0]))
    print(nn)
    results.append(nn([0, 1, 0, 0, 1]))
    print(nn)
    results.append(nn([1, 0, 1, 0, 0]))
    print(nn)
    print(results)


test()
