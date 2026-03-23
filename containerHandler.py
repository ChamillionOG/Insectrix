import pygame
import random

class ContainerManager:
    def __init__(self, current_container, containers_list, screen, container_bugs, data):
        self.current_container = current_container
        self.containers_list = containers_list
        self.screen = screen

        self.container_name = self.current_container
        self.container_data = self.containers_list[self.current_container]

    def load_container(self, container_bugs, data):
        image = pygame.image.load(f"assets/images/containers/{self.container_name}.png").convert_alpha()
        image = pygame.transform.scale(image, (300, 520))

        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottomleft = (20, 1060)

        self.load_bugs(container_bugs, data)

    def load_bugs(self, container_bugs, data):
        container_bugs.clear()

        for bug, amount in data["container"]["bugs"].items():
            for _ in range(amount):
                #self.add_bug(bug)
                pass

    #def add_bug(self, container_bugs, bug_type, CreateBug):
       # x = self.rect.centerx - 50
       # y = self.rect.top + 20

       # bug = CreateBug(x, y, bug_type)

       # bug.velX = random.uniform(-2.5, 2.5)
       # bug.velY = 0

        #container_bugs.append(bug)

    def draw(self):
        pass