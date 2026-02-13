import pygame

from dictionaries.bugnetDefinitions import bugnet_definitions

cursor_icon = pygame.image.load("assets/ui/mouse_cursor.png")
cursor_icon = pygame.transform.scale(cursor_icon, (64, 64))
cursor_icon_rect = cursor_icon.get_rect()

class BugnetManager():
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

        self.angle = 0
        self.max_angle = 80
        self.swing_speed = 24
        self.last_swing_time = 0
        self.swinging = False
        self.returning = False
        self.visible = True

    def can_swing(self, data):
        current_time = pygame.time.get_ticks() / 1000
        bugnet_type = data["bugnet"]
        cooldown = bugnet_definitions[bugnet_type]["cooldown"]

        return(not self.swinging and not self.returning and current_time - self.last_swing_time >= cooldown)

    def swing(self, data):
        if self.can_swing(data):
            self.swinging = True
            self.last_swing_time = pygame.time.get_ticks() / 1000

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

        mouseX, mouseY = mouse.get_pos()
        self.rect = self.image.get_rect()

        if self.visible:
            self.rect.centerx = mouseX
            self.rect.centery = mouseY + 60
            screen.blit(self.image, self.rect)
        else:
            cursor_icon_rect.centerx = mouseX
            cursor_icon_rect.centery = mouseY
            screen.blit(cursor_icon, cursor_icon_rect)