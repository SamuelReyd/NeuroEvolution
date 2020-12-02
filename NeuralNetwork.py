import numpy as np
from scipy.special import expit

class NeuralNetwork:
    
    @staticmethod
    def get_random_neural_network(vec_sizes: list):
        layers = list()
        for i in range(len(vec_sizes)-1):
            layers.append(np.random.uniform(-1, 1, (vec_sizes[i+1], vec_sizes[i] + 1)))
        return NeuralNetwork(layers, vec_sizes)
    
    def __init__(self, layers: list, layer_sizes: list):
        self.layers = layers
        self.shape = layer_sizes
        
        
    def feed_forward(self, input: list):
        vec = np.array(input).T
        for layer in self.layers:
            vec = expit(np.dot(layer[:, :-1], vec) + layer[:, -1])
        return vec