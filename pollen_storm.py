import pygame
import random
import math

class PollenParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(2, 5)
        self.speed = random.uniform(1, 3)
        self.sway_offset = random.uniform(0, 1000)
        self.life = 5000

    def update(self, dt, time):
        self.y += self.speed * dt * 60
        self.x += math.sin((time + self.sway_offset) * 0.002) * 0.5
        
        self.life -= dt * 1000

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 100), (self.x, self.y, self.size, self.size))