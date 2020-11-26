from Constants import *
from Pipe import Pipe
from Bird import Bird
import pygame
from pygame.locals import *
import numpy as np


SET_FPS = 500


def run(population, show_render):
    RUN = True
    pygame.display.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    pipes = [Pipe(Pipe.first_y)]
    birds = [Bird() for _ in range(POPULATION_SIZE)]
    scores = np.zeros(POPULATION_SIZE)  
    score = 0
    while RUN:
        # Rendering
        if (show_render) :
            clock.tick(SET_FPS)
            pygame.display.update()
            window.fill((255, 255, 255))
            for pipe in pipes:
                pygame.draw.rect(window, pipe.color, (pipe.x, 0, pipe.width, pipe.y))
                pygame.draw.rect(window, pipe.color, (pipe.x, pipe.y + pipe.gap, pipe.width, WINDOW_HEIGHT))
            for bird in birds:
                if bird.alive:
                    pygame.draw.circle(window, bird.color, (int(bird.x), int(bird.y)), bird.radius)
            
        # Events
        for event in pygame.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN :
                birds[0].up()
                    

        # Global state of the game

        near = pipes[0] if pipes[0].x + Pipe.width > birds[0].x else pipes[1]

        if pipes[-1].x<WINDOW_WIDTH - Pipe.space:
            pipes.append(Pipe(np.random.randint(10, WINDOW_HEIGHT - (Pipe.gap + 10))))

        if pipes[0].check_out():
            del pipes[0]
            score+=1
        for p in pipes:
            p.update(near)

        still_any = False     
        for i in range(POPULATION_SIZE):
            if birds[i].alive:
                still_any = True
                
                input = [
                birds[i].x / WINDOW_WIDTH, 
                birds[i].y / WINDOW_HEIGHT,
                birds[i].speed / birds[i].max_speed,
                near.x / WINDOW_WIDTH, 
                near.y / WINDOW_HEIGHT]
                
                output = population.feed_forward(i, input)
                if output > 0.5:
                    birds[i].up()
                birds[i].update()

                if birds[i].check_death(near) or score > 20 : # Bird lost or max score is reached (in order to avoir to long training time)
                    scores[i] = score
                    birds[i].alive = False

        if not still_any:
            return scores