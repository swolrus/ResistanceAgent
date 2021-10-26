from random import seed
from s22690264.network.layer import Layer


class Model:
    '''
    A basic ReLU activation neural net implementation
    Built with many thanks to Jason Brownlee from Machine Learning Mastery

    n_in is the number of inputs
    hidden is an int array representation of the hidden layers
    the hidden index is the layer and stored int is number of neurons
    n_out is the number of outputs

    nn contains the objects neural net dictionary
    '''
    def __init__(self, ran_seed, layers):
        self.first_run = False
        self.l_rate = None
        self.debug = False
        seed(ran_seed)
        self.activation_f = 'ReLU'
        self.nn = list()
        # Add one to each weight set meaning bias is the last weight
        # Randomise the weight set
        for i in range(len(layers) - 1):
            if i == 0:
                name = 'INPUT_LAYER '
            elif i == len(layers) - 2:
                name = 'OUTPUT_LAYER'
            else:
                name = 'HIDDEN_LAYER' + str(i)
            layer = Layer(layers[i], layers[i + 1], name)
            self.nn.append(layer)
        self.nn[-1].activation_f = 'sigmoid'

    def __str__(self):
        s = ''
        for layer in self.nn:
            s += str(layer)
        return s

    # Forward propagate input to a network output
    def forward_propagate(self, row):
        inputs = row
        for layer in self.nn:
            inputs = layer.propagate(inputs)
        return inputs

    # Backpropagate error and store in neurons
    def backward_propagate_error(self, expected):
        for i in reversed(range(len(self.nn))):
            layer = self.nn[i]
            errors = list()
            if i != len(self.nn) - 1:
                # if we are not at the output yet
                for j in range(len(self.nn[i].neurons)):
                    error = 0.0
                    for neuron in self.nn[i + 1].neurons:
                        error += (neuron['weights'][j] * neuron['error'])
                    errors.append(error)
            else:
                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(neuron['output'] - expected[j])
            for j in range(len(layer.neurons)):
                neuron = layer.neurons[j]
                neuron['error'] = errors[j] * layer.activation_dx(neuron['output'])

    # Update network weights with error
    def update_weights(self, row, l_rate):
        inputs = row
        for i in range(len(self.nn)):
            if i != 0:
                inputs = [neuron['output'] for neuron in self.nn[i - 1].neurons]
            for neuron in self.nn[i].neurons:
                for j in range(len(inputs)):
                    neuron['weights'][j] -= l_rate * neuron['error'] * inputs[j]
                neuron['weights'][-1] -= l_rate * neuron['error']

    # Train a network for a fixed number of epochs
    def train(self, rows, l_rate, n_epoch, n_outputs, anneal=False, anneal_rate=0.95, debug=False):
        if not self.first_run:
            self.l_rate = l_rate
            self.first_run = False

        for epoch in range(n_epoch):
            sum_error = 0
            for row in rows:
                outputs = self.forward_propagate(row)
                expected = [0 for i in range(n_outputs)]
                expected[row[-1]] = 1
                sum_error += sum([(expected[i] - outputs[i]) **
                                  2 for i in range(len(expected))])
                self.backward_propagate_error(expected)
                self.update_weights(row, self.l_rate)
            if anneal:
                self.l_rate = self.l_rate * anneal_rate
            if debug is True:
                print('epoch->%d, lrate is %.3f and error %.3f' % (epoch, l_rate, sum_error))

    def generator_train(self, generator, l_rate, n_epoch, anneal=False, anneal_rate=0.95, debug=False):
        if not self.l_rate:
            self.l_rate = l_rate
        for epoch in range(n_epoch):
            sum_error = 0
            rows = next(generator)
            # print(rows)
            for row in rows:
                x_train = row[0]
                y_train = row[1]
                outputs = self.forward_propagate(x_train)
                sum_error += sum([(y_train[i] - outputs[i]) **
                                  2 for i in range(len(y_train))])
                self.backward_propagate_error(y_train)
                self.update_weights(x_train, self.l_rate)
            if anneal:
                self.l_rate = self.l_rate * anneal_rate
            if debug is True:
                print('epoch->%d, lrate is %.3f and error %.3f' % (epoch, self.l_rate, sum_error))

    # Use the network to make a prediction
    def predict(self, row):
        return str(self.forward_propagate(row))
