from Constants import *
import pygame

class Pipe:
    gap = 250
    width = 100
    speed = -10
    space = 750
    first_y = 300
    def __init__(self, y):
        self.y = y
        self.x = WINDOW_WIDTH 
        self.color = (0, 255, 0)
    
    def update(self,near):
        self.x += self.speed
    
    def check_out(self):
        return self.x + self.width < 0