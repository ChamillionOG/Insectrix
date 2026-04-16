import pygame

class PopupText:
    def __init__(self, position, text, font, color, duration, scale=1.0):
        self.x, self.y = position
        self.start_y = self.y

        self.text = text
        self.font = font
        self.color = color

        self.duration = duration
        self.timer = 0

        self.alpha = 255
        self.base_scale = scale
        self.scale = scale

    def dead(self):
        return self.timer >= self.duration

    def update(self, scale):
        self.timer += 1

        progress = self.timer / self.duration
        progress = min(progress, 1)

        total_rise = 120 * scale
        self.y = self.start_y - (total_rise * progress)

        self.scale = self.base_scale + (0.25 * progress * scale)

        fade_start = 0.2
        if progress > fade_start:
            fade_progress = (progress - fade_start) / (1 - fade_start)
            self.alpha = max(0, 255 * (1 - fade_progress))

    def draw(self, screen, data):
        if not data["settings"]["popups"]:
            return

        text = self.font.render(self.text, False, self.color)

        text = pygame.transform.scale(text, (int(text.get_width() * self.scale), int(text.get_height() * self.scale),))

        text.set_alpha(int(self.alpha))

        rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, rect)