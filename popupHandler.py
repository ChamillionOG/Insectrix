import pygame

class PopupText:
    def __init__(self, position, text, color):
        self.x, self.y = position
        self.text = text
        self.color = color

        self.timer = 0
        self.alpha = 255

    def dead(self):
        return self.timer >= 60

    def update(self):
        self.timer += 1

        self.y += 2

        if self.timer > 15:
            self.alpha -= 10

            if self.alpha < 0:
                self.alpha = 0

    def draw(self, screen, font):
        surf = font.render(self.text, False, self.color)
        surf = pygame.transform.scale(
            surf,
            (
                int(surf.get_width() * self.scale),
                int(surf.get_height() * self.scale)
            )
        )

        surf.set_alpha(self.alpha)

        rect = surf.get_rect(center=(self.x, self.y))

        screen.blit(surf, rect)