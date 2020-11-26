import numpy as np

import keras

from NeuralNetwork import NeuralNetwork
from Constants import *

class GeneticAlgorithm :

    def __init__(self, vecSizes, popSize, mutationRate, crossoverNb, mutationScale, tensor = False) :
        self.popSize = popSize
        self.mutationRate = mutationRate
        self.crossoverNb = crossoverNb
        self.mutationScale = mutationScale
        self.tensor = tensor
        if tensor:
            self.population = list()
            for _ in range(popSize):
                model = keras.models.Sequential()
                model.add(keras.layers.Dense(vecSizes[1], input_dim = vecSizes[0]))
                for i in vecSizes[2:]:
                    model.add(keras.layers.Dense(i))
                self.population.append(model)

        else:
            self.population = [NeuralNetwork.get_random_neural_network(vecSizes) for i in range(popSize)]
        #self.population = [NeuralNetwork([np.array([[0, 0, 1, 0, -1, 0]])]) for i in range(popSize)]
    
    def feed_forward(self, i, input):
        brain = self.population[i]
        if self.tensor:
            return brain.predict(np.array([input]))
        else:
            return brain.feed_forward(input)

    def crossover(self, neuralNetwork1, neuralNetwork2) :
        if self.tensor:
            layers1, layers2 = list(), list()
            for i in range(0, len(neuralNetwork1.get_weights()), 2):
                w0 = neuralNetwork1.get_weights()[i]
                w1 = np.array([neuralNetwork1.get_weights()[i+1]])
                layers1.append(np.concatenate((w0, w1), axis = 0))

                w0 = neuralNetwork2.get_weights()[i]
                w1 = np.array([neuralNetwork2.get_weights()[i+1]])
                layers2.append(np.concatenate((w0, w1), axis = 0))
        else:
            layers1, layers2 = neuralNetwork1.layers, neuralNetwork2.layers

        newLayers = []
        for layer1, layer2 in zip(layers1, layers2) :
            flatLayer1 = np.reshape(layer1, -1)
            flatLayer2 = np.reshape(layer2, -1)
            crossoverPoints = sorted(np.random.choice(np.arange(len(flatLayer1)), self.crossoverNb, replace = False))
            crossoverPoints = [0] + crossoverPoints
            crossoverPoints.append(len(flatLayer1))
            newFlatLayer = []
            for i in range(len(crossoverPoints) - 1) :
                if i % 2 == 0 :
                    newFlatLayer.extend(flatLayer1[crossoverPoints[i] : crossoverPoints[i+1]])
                else :
                    newFlatLayer.extend(flatLayer2[crossoverPoints[i] : crossoverPoints[i+1]])
            self.mutation(newFlatLayer)

            if self.tensor:
                newLayer = np.reshape(np.array(newFlatLayer), layer1.shape)
                newLayer = [newLayer[:-1, :], newLayer[-1, :].flatten()]
            else:
                newLayer = np.reshape(np.array(newFlatLayer), layer1.shape)

            newLayers.append(newLayer)
        if self.tensor:
            model = keras.models.Sequential()
            model.add(keras.layers.Dense(LAYER_SIZES[1], input_dim = LAYER_SIZES[0]))
            for i in LAYER_SIZES[2:]:
                model.add(keras.layers.Dense(i))
            weights = list()
            for layer in newLayers:
                weights += layer
            model.set_weights(weights)
            return model
        else:
            return NeuralNetwork(newLayers)

    def mutation(self, flatLayer) :
        for pos in range(len(flatLayer)) :
            if (np.random.rand() < self.mutationRate) :
                if (MUTATION_SCALE >= 0) :
                    flatLayer[pos] = flatLayer[pos] + self.mutationScale*np.random.uniform(-1, 1)
                else :
                    flatLayer[pos] = np.random.uniform(-1, 1)
            
    
    def update(self, scores) :
        newPop = []
        # for i in range(self.popSize) :
        #     parent1, parent2 = np.random.choice(self.population, 2, p = scores/np.sum(scores), replace = False)
        #     newPop.append(self.crossover(parent1, parent2))
        possibleParents = sorted(self.population, key=lambda x: scores[self.population.index(x)])[-NB_OF_CHOSEN:]
        newPop.extend(possibleParents)
        for _ in range(NB_OF_CHOSEN, self.popSize):
            father, mother = np.random.choice(possibleParents, 2)
            newPop.append(self.crossover(father, mother))
        self.population = newPop