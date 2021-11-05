from random import seed
import math
from datetime import datetime
from s22690264.network.layer import Layer
from s22690264.network.generator import Generator
from decimal import Decimal


class Model:
    '''
    A basic ReLU activation neural net implementation
    Built with thanks to Jason Brownlee from Machine Learning Mastery

    n_in is the number of inputs
    hidden is an int array representation of the hidden layers
    the hidden index is the layer and stored int is number of neurons
    n_out is the number of outputs

    nn contains the objects neural net dictionary
    '''
    def __init__(self, layers, activation_f='ReLU'):
        self.layer_counts = layers
        self.gen = Generator()
        seed(datetime.now())
        self.first_run = True
        self.activation_f = activation_f

        self.l_rate = 0.3
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.t = 0

        self.outputs = 0
        self.nn = []
        self.in_l = Layer(None, self.layer_counts[0], 'INPUT', 0, None)
        self.nn.append(self.in_l)

        for i in range(1, len(self.layer_counts)):
            if i == len(self.layer_counts) - 1:
                self.out_l = Layer(self.nn[-1], self.layer_counts[i], 'OUTPUT', i, self.activation_f)
                self.nn.append(self.out_l)
            else:
                layer = Layer(self.nn[-1], self.layer_counts[i], 'HIDDEN', i, 'sigmoid')
                self.nn.append(layer)

    def __str__(self):
        s = ''
        for layer in self.nn:
            s += str(layer)
        return s

    def __call__(self, row):
        '''
        Forward propegates inputs through the entire network
        row is the inputes we wish to propegate
        returns the output of the output layer
        '''
        inputs = row
        if len(inputs) != self.in_l.n_in:
            raise ValueError('This network requires input of length {}, your data is of length {}'
                             .format(self.in_l.n_out, len(row)))
        for layer in self.nn:
            if layer.type != 0:
                # then each layer will take and forward propagate them
                row = layer(inputs)
            else:
                # first we set input layer outputs to be the row
                for i in range(len(layer.neurons)):
                    layer.neurons[i]['output'] = inputs[i]
        return row

    def get_outputs(self):
        '''
        returns the current outputs of the ouput layer
        '''
        return [n['output'] for n in self.l_output.neurons]

    def backward_propagate_error(self, expected):
        for i in reversed(range(len(self.nn) - 1)):
            layer = self.nn[i]
            errors = list()
            if i != len(layer.neurons) - 1:
                # if we are not at the output yet
                for j in range(len(layer.neurons)):
                    error = 0.0
                    for neuron in self.nn[i + 1].neurons:
                        error = neuron['weights'][j] * layer.activation_dx(neuron['delta'])
                    errors.append(error)
            else:
                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(neuron['output'] - expected[j])
            for j in range(len(layer.neurons)):
                layer.neurons[j]['delta'] = errors[j]

    # Update network weights with error
    def update_weights(self, row, l_rate):
        for i in range(len(self.nn)):
            inputs = row
            if i != 0:
                inputs = [neuron['output'] for neuron in self.nn[i - 1].neurons]
            for neuron in self.nn[i].neurons:
                for j in range(len(inputs)):
                    neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] -= l_rate * neuron['delta']

    def generator_train(self, n_epoch, n_minibatch, fold_size, debug=False):
        x_train, y_train = 0, 0
        for epoch in range(n_epoch):
            error = 0
            sum_error = 0
            self.gen.split_data(fold_size)
            mb = 0
            while mb < n_minibatch:
                mb += 1
                minibatch = next(self.gen)
                if minibatch is None:
                    break
                for x_train, y_train in minibatch:
                    self.outputs = self(x_train)
                    self.backward_propagate_error(y_train)
                    self.update_weights(x_train, self.l_rate)
                    sum_error += sum([math.sqrt((self.outputs[i] - y_train[i])**2) for i in range(self.out_l.n_out)])

                error += 1

            if debug is True and epoch % 10 == 0:
                print('epoch->{}, lrate is {} and error {}'.format(epoch, self.l_rate, sum_error / error))
        return False

    # Use the network to make a prediction
    def predict(self, row):
        # use the network to predict outputs for row, same as calling the object
        return self(row)
