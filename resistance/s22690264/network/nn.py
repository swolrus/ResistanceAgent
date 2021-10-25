from random import random, seed
import json


class NN:
    '''
    A basic ReLU activation neural net implementation
    Built with many thanks to Jason Brownlee from Machine Learning Mastery

    n_in is the number of inputs
    hidden is an int array representation of the hidden layers
    the hidden index is the layer and stored int is number of neurons
    n_out is the number of outputs

    nn contains the objects neural net dictionary
    '''
    def __init__(self, ran_seed, n_in, hidden, n_out):
        seed(ran_seed)
        self.nn = list()
        # Add one to each weight set meaning bias is the last weight
        # Randomise the weight set
        in_layer = [{'weights': [random() for i in range(n_in + 1)]}
                                for i in range(hidden[0])]
        self.nn.append(in_layer)

        for layer in range(1, len(hidden)):
            hidden_layer = [{'weights': [random() for i in range(hidden[layer - 1] + 1)]}
                            for i in range(hidden[layer])]
            self.nn.append(hidden_layer)

        out_layer = [{'weights': [random() for i in range(hidden[-1] + 1)]}
                     for i in range(n_out)]

        self.nn.append(out_layer)

    def __str__(self):
        s = ''
        for layer in range(len(self.nn)):
            if layer == len(self.nn) - 1:
                y = 'Output Layer'
            else:
                y = 'Hidden Layer {}'.format(layer)
            s += '{}\n {}\n'.format(y, json.dumps(self.nn[layer]))
        return s

    # Calculate neuron activation for an input
    def activation(self, weights, inputs):
        # take the bias
        a = weights[-1]
        for i in range(len(weights) - 1):
            # dot product of weights
            a += weights[i] * inputs[i]
        return a

    # Transfer the neuron activation
    # Using ReLu function
    def ReLU(self, a):
        return max(0.0, a)

    # Calculate the derivative of the ReLU function
    def drdx(self, x):
        if x < 0:
            return 0
        return 1

    # Forward propagate input to a network output
    def forward_propagate(self, row):
        inputs = row
        for layer in self.nn:
            new_inputs = []
            for neuron in layer:
                activation = self.activation(neuron['weights'], inputs)
                neuron['output'] = self.ReLU(activation)
                new_inputs.append(neuron['output'])
            inputs = new_inputs
        return inputs

    # Backpropagate error and store in neurons
    def backward_propagate_error(self, expected):
        for i in reversed(range(len(self.nn))):
            layer = self.nn[i]
            errors = list()
            if i != len(self.nn) - 1:
                # if we are not at the output yet
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self.nn[i + 1]:
                        error += (neuron['weights'][j] * neuron['delta'])
                    errors.append(error)
            else:
                for j in range(len(layer)):
                    neuron = layer[j]
                    errors.append(neuron['output'] - expected[j])
            for j in range(len(layer)):
                neuron = layer[j]
                neuron['delta'] = errors[j] * self.drdx(neuron['output'])

    # Update network weights with error
    def update_weights(self, row, l_rate):
        inputs = row[:-1]
        for i in range(len(self.nn)):
            if i != 0:
                inputs = [neuron['output'] for neuron in self.nn[i - 1]]
            for neuron in self.nn[i]:
                for j in range(len(inputs)):
                    neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
                neuron['weights'][-1] -= l_rate * neuron['delta']

    # Train a network for a fixed number of epochs
    def train_network(self, rows, l_rate, n_epoch, n_outputs, anneal=False, anneal_rate=0):

        for epoch in range(n_epoch):
            sum_error = 0
            for row in rows:
                outputs = self.forward_propagate(row)
                expected = [0 for i in range(n_outputs)]
                expected[row[-1]] = 1
                sum_error += sum([(expected[i] - outputs[i]) **
                                  2 for i in range(len(expected))])
                self.backward_propagate_error(expected)
                self.update_weights(row, l_rate)
            # print('epoch->%d, lrate is %.3f and error %.3f' % (epoch, l_rate, sum_error))

    # Use the network to make a prediction
    def predict(self, row):
        out = self.forward_propagate(row)
        return out
