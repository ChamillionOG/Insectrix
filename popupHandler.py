import pygame

class PopupText:
    def __init__(self, position, text, font, color, scale=1.0):
        self.x, self.y = position
        self.text = text
        self.font = font
        self.color = color

        self.timer = 0
        self.alpha = 255
        self.scale = scale

    def dead(self):
        return self.timer >= 60

    def update(self, scale):
        self.timer += 1

        self.y -= 2 * scale

        self.scale += 0.0025 * scale

        if self.timer > 15:
            self.alpha -= 10
            if self.alpha < 0:
                self.alpha = 0

    def draw(self, screen, data):
        if not data["settings"]["popups"]:
            return
        
        text = self.font.render(self.text, False, self.color)

        text = pygame.transform.scale(text, (int(text.get_width() * self.scale), int(text.get_height() * self.scale)))

        text.set_alpha(self.alpha)

        rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, rect)