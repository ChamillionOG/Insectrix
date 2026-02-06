import pygame

class UpgradeButton:
    def __init__(self, x, y, width, height, frame_image, icon_image, name, price, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.frame_image = pygame.transform.scale(frame_image, (width, height))
        self.icon_image = pygame.transform.scale(icon_image, (48, 48))
        self.name = name
        self.price = price
        self.font = font

        self.name_text = font.render(name, True, (255, 255, 255))
        self.price_text = font.render(f"{price}", True, (240, 240, 240))

    def draw(self, screen):
        screen.blit(self.frame_image, self.rect)
        screen.blit(self.icon_image, (self.rect.x + 10, self.rect.y +10))

        screen.blit(self.name_text, (self.rect.x + 70, self.rect.y + 10))
        screen.blit(self.price_text, (self.rect.x + 70, self.rect.y + 35))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class UpgradeManager:
    def __init__(self, x, y, spacing=10):
        self.buttons = []
        self.start_x = x
        self.start_y = y
        self.spacing = spacing

    def add_button(self, button):
        if not self.buttons:
            y = self.start_y
        else:
            last = self.buttons[-1]
            y = last.rect.bottom + self.spacing

        button.rect.topleft = (self.start_x, y)
        self.buttons.append(button)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                return button
            
        return None