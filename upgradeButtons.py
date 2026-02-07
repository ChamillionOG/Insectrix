import pygame

from savesManager import save_data

class UpgradeButton:
    def __init__(self, x, y, width, height, frame_image, icon_image, name, price, font):
        self.frame_image = pygame.transform.scale(frame_image, (width, height))
        self.rect = self.frame_image.get_rect(topleft=(x, y))
        self.icon_image = pygame.transform.scale(icon_image, (64, 64))
        self.name = name
        self.price = price
        self.font = font

        self.name_text = font.render(name, True, (255, 255, 255))
        self.price_text = font.render(f"{price}", True, (240, 240, 240))

    def draw(self, screen):
        screen.blit(self.frame_image, self.rect)
        screen.blit(self.icon_image, (self.rect.x + 125, self.rect.y + 150))

        screen.blit(self.name_text, (self.rect.x + 200, self.rect.y + 150))
        screen.blit(self.price_text, (self.rect.x + 200, self.rect.y + 185))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def can_afford(self, data):
        return data["currency"] >= self.price

class UpgradeManager:
    def __init__(self, margin_right, y, popup_manager, data, spacing=125):
        self.buttons = []
        self.margin_right = margin_right
        self.start_y = y
        self.popup_manager = popup_manager
        self.data = data
        self.spacing = spacing

    def add_button(self, button, screen_width):

        if not self.buttons:
            y = self.start_y
        else:
            last = self.buttons[-1]
            y = last.rect.top + self.spacing

        button.rect.topright = (screen_width - self.margin_right, y)

        self.buttons.append(button)

    def draw(self, screen):
        for button in reversed(self.buttons):
            button.draw(screen)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):

                if button.can_afford(self.data):
                    self.popup_manager.spawn("Purchased!", (0, 255, 0), button.rect.centerx - 275, button.rect.centery, 1)
                    self.data["currency"] -= button.price
                    save_data(self.data)
                else:
                    self.popup_manager.spawn("Can't Afford.", (255, 0, 0), button.rect.centerx - 275, button.rect.centery, 1)

                return button
            
        return None