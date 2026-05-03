import pygame
import random

class EnvironmentManager:
    def __init__(self, current_environment, environments_list):
        self.current_environment = current_environment
        self.environments_list = environments_list
        self.environment_name = self.current_environment

        self.target_environment = None
        self.start_flash = False
        self.end_flash = False
        self.changing = False
        self.intensity = 1
        self.timer = 0
        self.alpha = 0

    def load_environment(self, load_scaled, data):
        image = load_scaled(f"assets/images/environments/{self.environment_name}.png", 2560, 1440)
        data["environment_multiplier"] = self.environments_list[self.current_environment]["multiplier"]

        self.image = image
        self.rect = self.image.get_rect()

    def change_environment(self, screen_width, screen_height, upgrade_manager, buttons, load_scaled, data):
        if not self.changing: return

        if not self.start_flash:
            if self.intensity < 5:
                self.intensity *= 1.005
            else:
                self.intensity = 5
                self.start_flash = True

        if self.start_flash and not self.end_flash:
            self.alpha += 5
            self.alpha = min(self.alpha, 255)

            if self.alpha >= 255:
                self.alpha = 255
                data["environment"] = self.target_environment
                self.load_environment(load_scaled, data)
                upgrade_manager.organize_buttons(buttons)
                self.timer += 1

        if self.timer >= 250:
            self.end_flash = True
            self.start_flash = False

        if self.end_flash:
            self.alpha -= 3
            self.alpha = max(0, self.alpha)

            self.intensity *= 0.1

            if self.intensity < 0.1:
                self.intensity = 0

            if self.alpha <= 1:
                self.target_environment = None
                self.end_flash = False
                self.changing = False
                self.timer = 0

        if self.intensity >= 1:
            shake_x = random.uniform(-self.intensity, self.intensity)
            shake_y = random.uniform(-self.intensity, self.intensity)

            self.rect = self.image.get_rect(center=((screen_width // 2) + shake_x, (screen_height // 2) + shake_y))
        elif self.intensity == 0:
            self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_white_screen(self, screen):
        if (self.start_flash or self.end_flash) and self.changing:
            white_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            white_surface.fill((255, 255, 255, self.alpha))
            screen.blit(white_surface, (0, 0))