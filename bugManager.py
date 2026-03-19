import pygame
import random
import json
import math

from savesManager import save_data
from dictionaries.bugDictionaries import bug_dictionaries
from dictionaries.enviromentDictionaries import enviroment_dictionaries

class Bug:
    def __init__(self, bug_type, x, y):
        self.image = pygame.image.load(bug_dictionaries[bug_type]["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.direction = random.choice([-1, 1])
        self.speed = 3

        self.base_y = y
        self.amplitude = 50 # Higher = More Motion
        self.frequency = 0.05 # Smaller = Closer Waves
        self.var = 0
 
    def update(self, screen_width, screen):

        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1

        self.var += 1
        self.rect.y = self.base_y + int(self.amplitude * math.sin(self.frequency * self.var))

        screen.blit(self.image, self.rect)

class BugManager:
    def __init__(self, enviroment_name, on_screen_bugs, in_container_bugs, popup_manager):
        self.env_data = enviroment_dictionaries[enviroment_name]
        self.on_screen_bugs = on_screen_bugs
        self.in_container_bugs = in_container_bugs
        self.popup_manager = popup_manager

    def spawn_bug(self, screen_width, screen_height):
        bug_type = random.choice(self.env_data["bugs"])
        bug = Bug(bug_type, random.randint(0, screen_width - 128), random.randint(0, screen_height -128))
        self.on_screen_bugs.append(bug)
    
    def collect_bug(self, pos, container_rect, data, mouse, bugnet_manager):
        if not bugnet_manager.can_swing(data):
            return False

        mouseX, mouseY = mouse.get_pos()

        for bug in self.on_screen_bugs:
            if bug.rect.collidepoint(pos):
                if data["bugs"] < data["container"]["capacity"]:
                    self.on_screen_bugs.remove(bug)
                    bug.rect.midtop = (container_rect.centerx, container_rect.top + 20)
                    bug.velX = random.uniform(-2.5, 2.5)
                    bug.velY = 0

                    self.in_container_bugs.append(bug)
                    bugs = data["container"]["bugs"]
                    bugs[bug.type] = bugs.get(bug.type, 0) + 1
                    bug_name = bug_dictionaries[bug.type]["name"]
                    self.popup_manager.spawn(f"+1 {bug_name}", (255, 255, 255), mouseX, mouseY + 50, 1)

                    data["bugs"] += 1
                    save_data(data)
                    return True
                elif data["bugs"] == data["container"]["capacity"]:
                    self.popup_manager.spawn("You have a full container!", (255, 0, 0), mouseX, mouseY + 50, 1)
        return False
    
    def update(self, screen_width, screen):
        for bug in self.on_screen_bugs:
            bug.update(screen_width, screen)