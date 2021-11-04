from random import random, gauss
from math import exp, sqrt
from s22690264.common import util
from decimal import Decimal


class Layer:
    def __init__(self, previous, n_out, name, index, activation_f):
        if previous is not None:
            self.previous = previous
            self.n_in = self.previous.n_out
        else:
            self.previous = None
            self.n_in = n_out
        self.n_out = n_out
        self.type = util.LAYER_ID[name]
        self.name = name + '-' + str(index)
        self.activation_f = activation_f

        # Add one to each weight set meaning bias is the last weight
        # Randomise the weight set
        self.neurons = [{'weights': [0.0 if i == self.n_in else (random() * 2 * sqrt(2 / self.n_in)) for i in range(self.n_in + 1)], 'dw': 0.0, 'db': 0.0, 'v_dw': 0.0, 'v_db': 0.0, 's_dw': 0.0, 's_db': 0.0}
                        for i in range(self.n_out)]

    def __str__(self):
        s = self.name + ' (' + str(self.activation_f) + ')\n'
        for i in range(len(self.neurons)):
            s += '  Neuron' + str(i) + '//' + str(self.neurons[i]) + '\n'
        return s

    # Transfer the neuron activation
    # Using ReLu function
    def ReLU(self, x):
        return max(0.0, x)

    # Using the sigmoid function
    def sigmoid(self, x):
        return 1.0 / (1.0 + exp(-x))

    # Transfer derivitive
    # Using the ReLU function
    def drdx(self, x):
        if x < 0.0:
            return 0.0
        return 1.0

    # Using the Sigmoid function
    def dsdx(self, x):
        return x * (1.0 - x)

    # Calculate neuron activation for an input
    def activation(self, x):
        if self.activation_f == 'ReLU':
            return self.ReLU(x)
        if self.activation_f == 'sigmoid':
            return self.sigmoid(x)
        return x

    def activation_dx(self, x):
        if self.activation_f == 'ReLU':
            return self.drdx(x)
        if self.activation_f == 'sigmoid':
            return self.dsdx(x)
        return x

    def transfer(self, weights, row):
        inputs = row
        # take the bias
        a = weights[-1]
        for i in range(len(weights) - 1):
            # for each input calculate activation
            a += weights[i] * inputs[i]
        return a

    # Calculate neuron activation for an input
    def __call__(self, row):
        inputs = row
        outputs = []
        for neuron in self.neurons:
            a = self.transfer(neuron['weights'], inputs)
            outputs.append(self.activation(a))
            neuron['output'] = outputs[-1]
        return outputs
