from Constants import *
import pygame


class Bird:
    shock = -15
    radius = 5
    color = (255,0,0)
    max_speed = 10
    def __init__(self):
        self.x = WINDOW_WIDTH//10
        self.y = WINDOW_HEIGHT//2
        self.speed = 0
        self.score = 0
        self.alive = True
    
    def update(self):
        self.y += self.speed
        self.speed *= FRICTION
        self.speed += GRAVITY
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        
    
    def up(self):
        self.speed += self.shock
    
    def check_death(self, near):
        rect1=pygame.Rect(near.x, 0, near.width, near.y)
        rect2=pygame.Rect(near.x, near.y + near.gap,near.width, WINDOW_HEIGHT - (near.y + near.gap))

        if near.x <= self.x <= near.x + near.width and 0 < self.y <= near.y: return True
        if near.x <= self.x <= near.x + near.width and near.y + near.gap <= self.y <= WINDOW_HEIGHT: return True
        if self.y < self.radius or self.y > WINDOW_HEIGHT - self.radius: return True

        return False
