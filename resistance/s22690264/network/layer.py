from random import random, seed


class Layer:
    def __init__(self, in_out, prior_layer=None, activation='ReLU'):
        seed(1000)
        self.in_out = self.in_out
        self.activation_f = activation
        self.prior_layer = None
        self.ins = None
        self.outs = None

        if prior_layer is not None:
            if prior_layer.in_out[1] != self.in_out[0]:
                raise Exception("Incompatible inputs ({}) with previous layer outputs ({})!".format(
                    prior_layer.in_out[1], self.in_out[0]))

        # final value of weights is bias
        self.weights = [[random() for i in range(self.in_out[0])]
                        for i in range(self.in_out[1])]
        self.bias = [random() for i in range(self.in_out[1])]

    # Transfer the neuron activation
    # Using ReLu function
    def ReLU(self, a):
        return max(0.0, a)

    # Calculate the derivative of the ReLU function
    def drdx(self, x):
        if x < 0:
            return 0
        return 1

    # Calculate neuron activation for an input
    def prop_forward(self, inputs):
        # take the bias
        a = self.bias
        for i in range(len(self.weights) - 1):
            # dot product of weights
            a += self.weights[i] * inputs[i]
        return a

    def descend(self, grads_w, grads_b, steps):
        self.weights -= setps*grads_w
        self.
