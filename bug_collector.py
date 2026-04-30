import pygame
import random
import math

class BugCollector:
    def __init__(self, image, position):
        self.pos = pygame.Vector2(position)
        self.start_pos = pygame.Vector2(position)
        self.image = image
        self.target = None

    def choose_target(self, bugs):
        if bugs:
            self.target = random.choice(bugs)
        else:
            self.target = None

    def update(self, bugs, speed, data, collect_bug, container_rect, bugnet_manager, popups, scale, font, PopupText):
        if self.target not in bugs:
            self.choose_target(bugs)

        if self.target:
            target_pos = pygame.Vector2(self.target.rect.center)
            direction = target_pos - self.pos
            distance = direction.length()

            if distance != 0:
                direction = direction.normalize()
            
            self.pos += direction * speed

            if distance < (50 * scale):
                center = self.target.rect.center

                collect_bug(center, pygame.time.get_ticks(), data, container_rect, bugnet_manager, bugs, popups, scale, font, PopupText, True)

                self.target = None
        else:
            direction = self.start_pos - self.pos
            distance = direction.length()

            if distance > speed:
                direction = direction.normalize()

                self.pos += direction * speed
            else:
                self.pos = self.start_pos.copy()
    
    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.pos))