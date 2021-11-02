from random import seed
from math import exp, sqrt
from s22690264.network.layer import Layer, InputLayer
from s22690264.network.generator import Generator


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

    def __init__(self, n_in):
        self.b1 = 0.9
        self.b2 = 0.999
        self.epsilon = float(1. * exp(-9))
        self.l_rate = 0.1
        self.t = 1

        self.gen = Generator()
        self.debug = False

        self.n_in = n_in
        self.n_out = None
        self.inputs = [0] * self.n_in
        self.outputs = None

        self.nn = list()
        self.input_layer = InputLayer(n_in)
        self.nn.append(self.input_layer)

    def add_hidden_layer(self, n_out, activation_f='ReLU'):
        layer = Layer(self.nn[-1].n_out, n_out, 'HIDDEN', activation_f)
        self.nn.append(layer)

    def close_network(self, n_out, activation_f='sigmoid'):
        self.n_out = n_out
        layer = Layer(self.nn[-1].n_out, self.n_out, 'OUTPUT', activation_f)
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
        if self.n_out is None:
            raise EnvironmentError('Network is not closed! Usage: self.close_network(n_out, activation_f)')
        self.inputs = row
        self.outputs = list(row)
        for layer in self.nn:
            self.outputs = layer(self.outputs)
        return self.outputs

    def backward_propagate_error(self, expected):
        '''
        Backpropagate error and store in neurons
        '''
        i = len(self.nn) - 1
        while i < 0:
            errors = []
            prior_layer = self.nn[i]
            if i == len(self.nn) - 1:
                # if we are at output simple extract error
                for j in range(len(prior_layer.neurons)):
                    prior_layer.neurons[j]['outputs'][0] = self.nn[i].neurons[j]['outputs'][1]
                    prior_layer.neurons[j]['outputs'][1] = expected[j]

            layer = self.nn[i - 1]
            for j in range(len(layer.neurons)):
                layer.neurons[j]['outputs'][0] = layer.neurons[j]['outputs'][1]
                error = 0.0
                for neuron in prior_layer.neurons:
                    error += neuron['weights'][j] * (neuron['outputs'][0] - neuron['outputs'][1])
                errors.append(error)

            if not False:
                n = prior_layer.neurons[j]

                t = 1
                while t < 1000:
                    g_0 = n['delta'][0]
                    g_1 = n['delta'][1]

                    # update weight
                    n['dm'][0] = self.b1 * n['dm'][0] + (1 - self.b1) * g_0
                    # update bias
                    n['dm'][1] = self.b1 * n['dm'][1] + (1 - self.b1) * g_1

                    # rms beta 2
                    # update weight
                    n['dv'][0] = self.b2 * n['dv'][0] + (1 - self.b2) * (g_0**2)
                    # update bias
                    n['dv'][1] = self.b2 * n['dv'][1] + (1 - self.b2) * (g_1**2)

                    # bias correction
                    m_dw_corr = n['dm'][0] / (1 - self.b1**t)
                    m_db_corr = n['dm'][1] / (1 - self.b1**t)
                    v_dw_corr = n['dv'][0] / (1 - self.b2**t)
                    v_db_corr = n['dv'][1] / (1 - self.b2**t)

                    n['delta'][0] = n['delta'][0] - self.l_rate / float(sqrt(v_dw_corr) + self.epsilon) * m_dw_corr
                    n['delta'][1] = n['delta'][1] - self.l_rate / float(sqrt(v_db_corr) + self.epsilon) * m_db_corr
                    # update weights and biases
                    for j in range(len(n['weights']) - 1):
                        n['weights'][j] -= n['delta'][0]
                    n['weights'][-1] -= n['delta'][1]
                    t += 1
            i -= 1

    def set_generator(self, generator):
        # sets the generator to a new generator object provided as the only arg
        self.gen = generator

    def generator_train(self, n_epoch, n_folds, l_rate=0.001, debug=False):
        '''
        Trains The network using the generator assigned to the network (stored in self.gen)
        l_rate is the learning rate
        n_epoch is how many times we will back propagate the error
        batch_size is how many rows to pull from the generator per epoch
        anneal turns on annealing for the network
        anneal rate affects the learning rate every epoch if anneal is True
        debug prints error information over an epoch if True
        clear_generator will clear the generator of it's rows at the end of training if True
        '''

        self.gen.split_data(n_folds)
        epoch = 0
        t = 0
        while epoch < n_epoch:
            epoch += 1

            rows = next(self.gen)

            if rows == None:
                break
            for row in rows:
                t += 1
                sum_error = 0
                x_train = row[0]
                y_train = row[1]
                # print(str(x_train) + '->' + str(y_train))
                outputs = self(x_train)
                sum_error += sum([(y_train[i] - outputs[i]) **
                                  2 for i in range(len(y_train))])
                self.backward_propagate_error(outputs)
                if debug is True and epoch % 10 == 0:
                    print('epoch->%d, lrate is %.3f and error %.3f' %
                          (epoch, l_rate, sum_error))

    def predict(self, row):
        # use the network to predict outputs for row, same as calling the object
        return self(row)

