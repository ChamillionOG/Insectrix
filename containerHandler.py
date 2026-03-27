import pygame
import random

class ContainerManager:
    def __init__(self, current_container, containers_list, screen, container_bugs, data):
        self.current_container = current_container
        self.containers_list = containers_list
        self.screen = screen

        self.container_name = self.current_container
        self.container_data = self.containers_list[self.current_container]

    def load_container(self, container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data):
        image = load_scaled(f"assets/images/containers/{self.container_name}.png", 300, 520)

        self.original_image = image
        self.image = image
        self.rect = image.get_rect(bottomleft=scale_position(20, 1420))

        self.load_bugs(container_bugs, load_scaled, bugs_list, scale, Bug, data)

    def load_bugs(self, container_bugs, load_scaled, bugs_list, scale, Bug, data):
        container_bugs.clear()

        for bug_key, amount in data["container"]["bugs"].items():
            bug_data = bugs_list[bug_key]

            for _ in range(amount):
                self.add_bug(container_bugs, bug_data, load_scaled, Bug)

        capacity = data["container"]["capacity"]

        inner_rect = self.rect
        inner_height = inner_rect.height - (125 * scale)
        spacing = inner_height / capacity

        for i, bug in enumerate(container_bugs):
            bug.targetY = inner_rect.bottom - (i * spacing)

            bug.rect.bottom = bug.targetY
            bug.velY = 0

    def add_bug(self, container_bugs, bug_data, load_scaled, Bug):
        x = self.rect.centerx
        y = self.rect.top

        bug = Bug((x, y), load_scaled,  bug_data)

        bug.in_container = True
        bug.velX = random.uniform(-5, 5)
        bug.velY = 0

        container_bugs.append(bug)

    def draw(self, container_bugs, screen, scale, screen_width):
        inner_rect = self.rect.inflate(int(-10 * scale), int(-10 * scale))

        for bug in container_bugs:
            bug.draw(scale, screen, screen_width, inner_rect)

        screen.blit(self.image, self.rect)