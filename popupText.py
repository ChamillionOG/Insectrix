import pygame

pygame.font.init()

font = pygame.font.Font("assets/Pixel.ttf", 50)
clock = pygame.time.Clock()

class PopupText:
    def __init__(self, text, color, x, y, font, duration):
        self.text = text
        self.color = color
        self.posX = x
        self.posY = y
        self.font = font

        self.fadeY = -40
        self.alpha = 255

        self.duration = duration
        self.time_left = duration

        self.message = self.font.render(self.text, True, self.color)
        self.rect = self.message.get_rect(center=(x, y))

    def update(self, dt):
        self.time_left -= dt
        self.posY += self.fadeY * dt

        self.alpha = int(255 * (self.time_left / self.duration))
        self.alpha = max(0, self.alpha)

        self.message.set_alpha(self.alpha)
        self.rect.center = (int(self.posX), int(self.posY))

    def draw(self, screen):
        screen.blit(self.message, self.rect)

    def dead(self):
        return self.time_left <= 0
    
class PopupTextManager:
    def __init__(self):
        self.popups = []

    def spawn(self, text, color, x, y, duration):
        self.popups.append(PopupText(text, color, x, y, font, duration))

    def update(self, dt):
        for popup in self.popups[:]:
            popup.update(dt)
            if popup.dead():
                self.popups.remove(popup)

    def draw(self, screen):
        for popup in self.popups:
            popup.draw(screen)