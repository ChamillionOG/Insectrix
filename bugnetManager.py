import pygame

class BugnetManager():
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

        self.angle = 0
        self.max_angle = 60
        self.swing_speed = 24
        self.swinging = False
        self.returning = False

    def swing(self):
        if not self.swinging and not self.returning:
            self.swinging = True

    def update(self, screen, mouse, data):
        self.image = pygame.image.load(f"assets/images/bugnets/{data["bugnet"]}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256, 256))

        if self.swinging:
            self.angle += self.swing_speed
            if self.angle >= self.max_angle:
                self.angle = self.max_angle
                self.swinging = False
                self.returning = True
        elif self.returning:
            self.angle -= self.swing_speed
            if self.angle <= 0:
                self.angle = 0
                self.returning = False

        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=mouse.get_pos())

        screen.blit(self.image, self.rect)