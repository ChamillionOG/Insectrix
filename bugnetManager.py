import pygame

from dictionaries.bugnetDictionaries import bugnet_dictionaries

cursor_icon = pygame.image.load("assets/ui/mouse_cursor.png")
cursor_icon = pygame.transform.scale(cursor_icon, (64, 64))
cursor_icon_rect = cursor_icon.get_rect()

class BugnetManager():
    def __init__(self, bugnet_type, rect):
        self.bugnet_type = bugnet_type
        self.load_bugnet(bugnet_type)
        self.rect = rect

        self.angle = 0
        self.max_angle = 80
        self.swing_speed = 24
        self.last_swing_time = 0
        self.swinging = False
        self.returning = False
        self.visible = True

    def load_bugnet(self, bugnet_type):
        loaded_image = pygame.image.load(f"assets/images/bugnets/{bugnet_type}.png").convert_alpha()
        loaded_image = pygame.transform.scale(loaded_image, (256, 256))

        self.base_image = loaded_image
        self.image = self.base_image

    def can_swing(self, data):
        current_time = pygame.time.get_ticks() / 1000
        bugnet_type = data["bugnet"]
        cooldown = bugnet_dictionaries[bugnet_type]["cooldown"]

        return(not self.swinging and not self.returning and current_time - self.last_swing_time >= cooldown)

    def swing(self, data):
        if self.can_swing(data):
            self.swinging = True
            self.last_swing_time = pygame.time.get_ticks() / 1000

    def update(self, screen, mouse, data):
        if data["bugnet"] != self.bugnet_type:
            self.bugnet_type = data["bugnet"]
            self.load_bugnet(self.bugnet_type)

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

        self.image = pygame.transform.rotate(self.base_image, self.angle)

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