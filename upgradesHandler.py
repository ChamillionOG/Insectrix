import pygame

class UpgradeButton:
    def __init__(self, position, config, load_scaled, font):
        self.x, self.y = position
        self.config = config

        self.name = self.config["name"]
        self.icon = load_scaled(self.config["icon"], 78, 78)
        self.cost = self.config["cost"]
        self.data = self.config["data"]
        self.amount = self.config["amount"]
        self.one_time = self.config["one_time"]

        self.frame = load_scaled("assets/ui/upgrade_button_frame.png", 410.4, 169.6)
        self.cover = load_scaled("assets/ui/upgrade_cover_frame.png", 410.4, 169.6)

        self.name_text = font("ThinBold", 25).render(f"{self.name}", False, (255, 255, 255))
        self.cost_text = font("Thin", 20).render(f"{self.cost} Insectra", False, (255, 255, 255))

        self.rect = self.frame.get_rect(center=(self.x, self.y))

    def can_afford(self, data):
        return data["currency"] >= self.cost

    def draw(self, screen, data):
        if self.can_afford(data):
            screen.blit(self.frame, self.rect)
        else:
            screen.blit(self.cover, self.rect)
        
        screen.blit(self.icon, (self.x - 190, self.y - 5))
        screen.blit(self.name_text, (self.x - 115, self.y + 10))
        screen.blit(self.cost_text, (self.x - 115, self.y + 40))