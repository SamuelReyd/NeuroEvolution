import time
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from Constants import *
from Bird import Bird
from Pipe import Pipe
from GeneticAlgorithm import GeneticAlgorithm
from run import run

SHOW_RENDER = True
SAVE_BEST_PLAYER = True
NB_OF_GENERATION = 50


os.chdir("/Users/samuelreyd/Documents/Projet/NeuroEvolution")


population = GeneticAlgorithm(LAYER_SIZES, POPULATION_SIZE, MUTATION_RATE, CROSSOVER_NUMBER, MUTATION_SCALE, True)
generation = 0

score = 0

best_scores = list()
average_scores = list()

for _ in range(NB_OF_GENERATION):
    scores = run(population, SHOW_RENDER)
    if scores is None:
        break
    print(f"Generation n°{generation}, mean score : {np.mean(scores)}, max score : {np.max(scores)}")

    best_scores.append(np.max(scores))
    average_scores.append(np.mean(scores))
    generation += 1
    population.update(scores)


plt.plot(range(len(best_scores)), best_scores)
plt.plot(range(len(average_scores)), average_scores)
plt.savefig("image"+str(len(os.listdir())))