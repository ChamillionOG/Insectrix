import pygame
import random

from bugManager import Bug

class ContainerManager:
    def __init__(self, container_data, screen_height, in_container_bugs, data):
        self.container_data = container_data
        self.in_container_bugs = in_container_bugs

        self.container_image = pygame.image.load(f"assets/images/containers/{data['container']['type']}.png").convert_alpha()
        self.container_image = pygame.transform.scale(self.container_image, (640, 640))

        self.container_image_rect = self.container_image.get_rect()
        self.container_image_rect.bottomleft = (-100, screen_height)

        self.bug_count = data["bugs"]

    def update(self, screen):
        for i, bug in enumerate(self.in_container_bugs):
            container_floor = (self.container_image_rect.bottom - (i + 1) * ((100 // self.container_data["capacity"]) * 4) - self.container_data["offset"])

            bug.velY += bug.gravity
            bug.rect.y += bug.velY
            bug.rect.x += bug.velX

            if bug.rect.left <= self.container_image_rect.left + 16:
                bug.rect.left = self.container_image_rect.left + 16
                bug.velX *= -0.5
            elif bug.rect.right >= self.container_image_rect.right - 16:
                bug.rect.right = self.container_image_rect.right - 16
                bug.velX *= -0.5

            if bug.rect.bottom >= container_floor:
                bug.rect.bottom = container_floor
                bug.velY = 0
                bug.velX *= 0.85

                if abs(bug.velX) < 0.1:
                    bug.velX = 0

            screen.blit(bug.image, bug.rect)

        screen.blit(self.container_image, self.container_image_rect)

    def loadBugs(self, data):
        self.in_container_bugs.clear()

        for bug_type, count in data["container"]["bugs"].items():
            for _ in range(count):
                x = self.container_image_rect.centerx - 50
                y = self.container_image_rect.top + 20

                bug = Bug(bug_type, x, y)
                bug.velX = random.uniform(-2.5, 2.5)
                bug.velY = 0

                self.in_container_bugs.append(bug)