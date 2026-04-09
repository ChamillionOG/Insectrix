import pygame

class UpgradeButton:
    def __init__(self, position, config, load_scaled, scale_position, font):
        self.x, self.y = position
        self.config = config

        self.name = self.config["name"]
        self.icon = load_scaled(self.config["icon"], 64, 64)
        self.cost = self.config["cost"]
        self.data = self.config["data"]
        self.amount = self.config["amount"]
        self.one_time = self.config["one_time"]

        self.frame = load_scaled("assets/ui/upgrade_button_frame.png", 342, 212)
        self.cover = load_scaled("assets/ui/upgrade_cover_frame.png", 342, 212)

        self.name_text = font("Regular", 12)
        self.cost_text = font("Thin", 8)

        self.rect = self.frame.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.frame, self.rect)