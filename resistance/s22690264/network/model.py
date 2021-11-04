from random import seed
from math import sqrt, pow
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
    def __init__(self, layers, activation_f='Sigmoid'):
        self.layer_counts = layers
        self.gen = Generator()
        seed(datetime.now())
        self.first_run = True
        self.activation_f = activation_f

        self.nn = []
        self.in_l = Layer(None, self.layer_counts[0], 'INPUT', 0, None)
        self.nn.append(self.in_l)

        for i in range(1, len(self.layer_counts)):
            if i == len(self.layer_counts) - 1:
                self.out_l = Layer(self.nn[-1], self.layer_counts[i], 'OUTPUT', i, self.activation_f)
                self.nn.append(self.out_l)
            else:
                layer = Layer(self.nn[-1], self.layer_counts[i], 'HIDDEN', i, 'ReLU')
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
                    layer.neurons[i]['output'] = row[i]
        return row

    def get_outputs(self):
        '''
        returns the current outputs of the ouput layer
        '''
        return [n['output'] for n in self.l_output.neurons]

    def backward_propagate_error(self, expected):
        for i in reversed(range(len(self.nn))):
            layer = self.nn[i]
            errors = list()
            if i != len(self.nn) - 1:
                # if we are not at the output yet
                for j in range(len(layer.neurons)):
                    error = Decimal('0.0')
                    for neuron in self.nn[i + 1].neurons:
                        error += Decimal(neuron['weights'][j]) * neuron['dw']
                    errors.append(error)
            else:
                for j in range(len(layer.neurons)):
                    neuron = layer.neurons[j]
                    errors.append(neuron['output'] - expected[j])
            for j in range(len(layer.neurons)):
                neuron = layer.neurons[j]
                neuron['dw'] = errors[j] * layer.activation_dx(neuron['output'])
                neuron['db'] = errors[j]

    # Update network weights with error
    def update_weights(self, t, l_rate, beta1, beta2, epsilon):
        for i in range(0, len(self.nn)):
            for neuron in self.nn[i].neurons:
                if t == 1:
                    neuron['v_dw'], neuron['v_db'] = 0.0, 0.0
                    neuron['s_dw'], neuron['s_db'] = 0.0, 0.0

                # ADAMS OPTIMISER
                # Momentum calculations
                neuron['v_dw'] = beta1 * neuron['v_dw'] + (1.0 - beta1) * neuron['dw']
                neuron['v_db'] = beta1 * neuron['v_db'] + (1.0 - beta1) * neuron['db']

                # RMS Calcs
                neuron['s_dw'] = beta2 * neuron['s_dw'] + (1.0 - beta2) * (neuron['dw']**2)
                neuron['s_db'] = beta2 * neuron['s_db'] + (1.0 - beta2) * (neuron['db'])

                # Bias Correction
                v_dw_corr = neuron['v_dw'] / (1.0 - pow(beta1, t))
                v_db_corr = neuron['v_db'] / (1.0 - pow(beta1, t))
                s_dw_corr = neuron['s_dw'] / (1.0 - pow(beta2, t))
                s_db_corr = neuron['s_db'] / (1.0 - pow(beta1, t))

                neuron['dw'] = l_rate * v_dw_corr / (sqrt(s_dw_corr) + epsilon)
                neuron['db'] = l_rate * v_db_corr / (sqrt(s_db_corr) + epsilon)

                # Update Weights
                for j in range(len(self.nn[i - 1].neurons) - 1):
                    neuron['weights'][j] -= neuron['dw']
                neuron['weights'][-1] -= neuron['db']

    def generator_train(self, n_epoch, batch_size, debug=False):
        l_rate = 0.001
        beta1 = 0.9
        beta2 = 0.999
        epsilon = 0.0000001
        t = 0.0
        for epoch in range(n_epoch):
            t += 1.0
            self.gen.split_data(batch_size)
            error = 0.0
            minibatch = next(self.gen)
            if minibatch is None:
                break

            for row in minibatch:
                x_train = row[0]
                y_train = row[1]
                outputs = self(x_train)

            error = sum([(outputs[i] - y_train[i])**2 - 2*(outputs[i] - y_train[i]) + 1 for i in range(self.out_l.n_out)])

            self.backward_propagate_error(y_train)
            self.update_weights(t, l_rate, beta1, beta2, epsilon)

            if debug is True and epoch % 10 == 0:
                print('epoch->{}, lrate is {} and error {}'.format(epoch, l_rate, error))
            if error < 0.01:
                return
    def loss_function(m):
        return m**2 - 2 * m + 1

    # take derivative
    def grad_function(m):
        return 2 * m - 2

    def check_convergence(w0, w1):
        return (w0 == w1)

    # Use the network to make a prediction
    def predict(self, row):
        # use the network to predict outputs for row, same as calling the object
        return self(row)
