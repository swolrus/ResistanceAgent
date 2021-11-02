from random import random, seed
from math import exp


class Layer:
    def __init__(self, n_in, n_out, name='HIDDEN', activation_f='ReLU'):
        self.name = name
        self.n_in = n_in
        self.n_out = n_out
        self.activation_f = activation_f

        # final value of weights is bias
        self.neurons = [{'weights': [random() for i in range(self.n_in + 1)], 'dm': [0., 0.], 'dv': [0., 0.], 'g': [0., 0.], 'delta': [0, 0], 'outputs': [0., 0]}
                        for i in range(self.n_out)]

    def __str__(self):
        s = self.name + ' (' + self.activation_f + ')\n'
        for i in range(len(self.neurons)):
            s += '    Neuron' + str(i) + ' // ' + str(self.neurons[i]) + '\n'
        return s

    # Transfer the neuron activation
    # Using ReLu function
    def ReLU(self, a):
        r = max(0., a)
        return r

    # Using the sigmoid function
    def sigmoid(self, x):
        r = 1. / (1. + exp(-x))
        return r

    # Transfer derivitive
    # Using the ReLU function
    def drdx(self, x):
        if x < 0:
            return 0.
        return 1.

    # Using the Sigmoid function
    def dsdx(self, x):
        r = x * (1. - x)
        return r

    # Calculate neuron activation for an input
    def activation(self, weights, inputs):
        self.inputs = list(inputs)
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
        outputs = list()
        for neuron in self.neurons:
            activation = self.activation(neuron['weights'], inputs)
            outputs.append(activation)
            neuron['outputs'][0] = neuron['outputs'][1]
            neuron['outputs'][1] = activation
        return outputs


class InputLayer(Layer):
    def __init__(self, n_in, name='INPUT'):
        self.activation_f = 'N/A'
        self.previous = None
        self.name = name
        self.n_in = n_in
        self.n_out = n_in
        self.inputs = [0] * self.n_out
        self.neurons = [{'weights': [random()], 'delta': [0., 0.], 'dm': [0., 0.], 'dv': [0., 0.], 'outputs': [0., 0.]} for i in range(self.n_in)]

    # Calculate neuron activation for an input
    def __call__(self, inputs):
        if self.n_out != len(inputs):
            raise AttributeError('Input of length {0} does not match layer {1} input length {2}!'
                                 .format(str(len(inputs)), str(self), str(self.n_in)))

        self.inputs = inputs.copy()
        self.outputs = []
        for i in range(len(inputs)):
            self.neurons[i]['outputs'][0] = self.neurons[i]['outputs'][1]
            self.neurons[i]['outputs'][1] = inputs[i]
            self.outputs.append(inputs[i])
        return inputs
