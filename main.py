import time
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from Bird import Bird
from Pipe import Pipe
from GeneticAlgorithm import GeneticAlgorithm
from run import run

SHOW_RENDER = False
SAVE_BEST_PLAYER = True
TF = False

abs_path = "/Users/samuelreyd/Documents/Projet/NeuroEvolution"
os.chdir(abs_path)

config_nb = 1

nb_tries = len(os.listdir(os.path.join("config" + str(config_nb)))) - 2
image_save_path = os.path.join("config" + str(config_nb), "try" + str(nb_tries))

config_path = os.path.join("config" + str(config_nb), "config.txt")
with open(config_path) as file:
    config_dict = eval(file.read())


NB_OF_GENERATION = config_dict["NB_OF_GENERATION"]
LAYER_SIZES = config_dict["LAYER_SIZES"]
POPULATION_SIZE = config_dict["POPULATION_SIZE"]
MUTATION_RATE = config_dict["MUTATION_RATE"]
CROSSOVER_NUMBER = config_dict["CROSSOVER_NUMBER"]
MUTATION_SCALE = config_dict["MUTATION_SCALE"]
NB_OF_CHOSEN = config_dict["NB_OF_CHOSEN"]


population = GeneticAlgorithm(LAYER_SIZES, POPULATION_SIZE, MUTATION_RATE, CROSSOVER_NUMBER, MUTATION_SCALE, NB_OF_CHOSEN, TF)
generation = 0

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
plt.savefig(image_save_path)