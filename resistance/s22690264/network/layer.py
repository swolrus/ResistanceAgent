from random import random, seed
from math import exp


class Layer:
    def __init__(self, n_in, n_out, name='Layer', activation='ReLU'):
        self.name = name
        self.n_in = n_in
        self.n_out = n_out
        self.activation_f = activation
        self.ins = None
        self.outs = None

        # final value of weights is bias
        self.neurons = [{'weights': [random() for i in range(self.n_in + 1)]}
                        for i in range(self.n_out)]

    def __str__(self):
        s = self.name + ' (' + self.activation_f + ')\n'
        for i in range(len(self.neurons)):
            s += '    Neuron' + str(i) + ' // ' + str(self.neurons[i]) + '\n'
        return s

    # Transfer the neuron activation
    # Using ReLu function
    def ReLU(self, a):
        return max(0.0, a)

    # Using the sigmoid function
    def sigmoid(self, x):
        return 1.0 / (1.0 + exp(-x))

    # Transfer derivitive
    # Using the ReLU function
    def drdx(self, x):
        if x < 0:
            return 0
        return 1

    # Using the Sigmoid function
    def dsdx(self, x):
        return x * (1.0 - x)

    # Calculate neuron activation for an input
    def activation(self, weights, inputs):
        # take the bias
        a = weights[-1]
        for i in range(len(weights) - 1):
            # for each input calculate activation
            a += weights[i] * inputs[i]

        if self.activation_f == 'ReLU':
            return self.ReLU(a)
        if self.activation_f == 'sigmoid':
            return self.sigmoid(a)
        return a

    def activation_dx(self, a):
        if self.activation_f == 'ReLU':
            return self.drdx(a)
        if self.activation_f == 'sigmoid':
            return self.dsdx(a)
        return a

    # Calculate neuron activation for an input
    def __call__(self, inputs):
        outputs = []
        for neuron in self.neurons:
            activation = self.activation(neuron['weights'], inputs)
            neuron['output'] = activation
            outputs.append(neuron['output'])
        return outputs
