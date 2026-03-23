import pygame

class EnvironmentManager:
    def __init__(self, screen_size, data):
        self.screen_size = screen_size
        self.image = None

        self.update_environment(data)

    def update_environment(self, data):
        image  = pygame.image.load(f"assets/images/environments/{data["environment"]}.png")
        image = pygame.transform.scale(image, self.screen_size)

        self.image = image