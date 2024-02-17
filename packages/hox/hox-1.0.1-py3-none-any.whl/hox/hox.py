import numpy as np
import pickle

class Sigmoid():
    def forward(self, x):
        return np.divide(np.float32(1), (np.float32(1) + np.exp(-x)))

    def backward(self, layer_output, delta):
        return np.multiply(delta, np.multiply(layer_output, (np.float32(1) - layer_output)))

    def initialize(self, neurons, input_neurons):
        return np.random.uniform(low=-0.1, high=0.1, size=(neurons, input_neurons)).astype(np.float32)

class Relu():
    def forward(self, x):
        return np.maximum(x, np.float32(0))

    def backward(self, layer_output, delta):
        return np.multiply(delta, (layer_output > np.float32(0)))

    def initialize(self, neurons, input_neurons):
        return np.random.normal(loc=0, scale=np.sqrt(2 / input_neurons), size=(neurons, input_neurons)).astype(np.float32)

class Layer():
    def __init__(self, input_neurons, neurons, activation):
        self.activation = activation
        self.weights = self.init_weights(neurons, input_neurons)
        self.biases = self.init_biases(neurons)

    def init_weights(self, neurons, input_neurons):
        return self.activation.initialize(neurons, input_neurons)

    def init_biases(self, neurons):
        return np.zeros(neurons, dtype=np.float32)

class Dense(Layer):
    def __init__(self, input_neurons, neurons, activation):
        super().__init__(input_neurons, neurons, activation)

    def forward(self, x):
        self.layer_output = self.activation.forward(np.add(np.dot(self.weights, x), self.biases))
        return self.layer_output

    def backward(self, delta):
        return self.activation.backward(self.layer_output, delta)

class Optimizer():
    def __init__(self, model, learning_rate):
        self.model = model
        self.learning_rate = learning_rate

    def zero_grad(self):
        self.grads_number = 0
        self.grads = []
        for layer in self.model.layers:
            self.grads += [[np.zeros_like(layer.weights), np.zeros_like(layer.biases)]]

    def grad(self, y, **options):
        for index in range(len(self.model.layers)-1, -1, -1):
            if index == len(self.model.layers)-1:
                delta = np.subtract(self.model.layers[index].layer_output, y)
            else:
                delta = np.dot(self.model.layers[index + 1].weights.T, delta)
            delta = self.model.layers[index].backward(delta)
            if index == 0:
                self.grads[index][0] += np.outer(delta, self.model.x)
            else:
                self.grads[index][0] += np.outer(delta, self.model.layers[index - 1].layer_output)
            self.grads[index][1] += delta
        self.grads_number += 1
        if options.get("x_gradient"):
            return np.dot(self.model.layers[0].weights.T, delta)

class SGD(Optimizer):
    def __init__(self, model, learning_rate):
        super().__init__(model, learning_rate)

    def step(self):
        factor = np.float32(1/self.grads_number*self.learning_rate)
        for index in range(len(self.model.layers)):
            self.model.layers[index].weights -= self.grads[index][0] * factor
            self.model.layers[index].biases -= self.grads[index][1] * factor

class Model():
    def __init__(self, layers):
        self.layers = layers

    @classmethod
    def create(cls, layers):
        return cls(layers)

    @classmethod
    def load(cls, name):
        with open(name + ".pkl", "rb") as file:
            layers = pickle.load(file)
        return cls(layers)

    def save(self, name):
        with open(name + ".pkl", "wb") as file:
            pickle.dump(self.layers, file)

    def run(self, x):
        self.x = x
        for layer in self.layers:
            x = layer.forward(x)
        return x
