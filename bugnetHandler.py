import pygame
import math

class BugnetManager:
    def __init__(self, current_bugnet, bugnets_list):
        self.current_bugnet = current_bugnet
        self.bugnets_list = bugnets_list

        self.swinging = False
        self.returning = False
        self.visible = True

        self.angle = 0
        self.max_angle = 120

        self.last_swing_time = 0
        self.swing_start_time = 0

        self.swing_duration = 0.25
        self.return_duration = 0.2

        self.bugnet_name = self.current_bugnet
        self.bugnet_data = self.bugnets_list[self.current_bugnet]

        self.original_image = None
        self.image = None
        self.rect = None

    def load_bugnet(self, load_scaled):
        image = load_scaled(f"assets/images/bugnets/{self.bugnet_name}.png", 256, 256)

        self.original_image = image
        self.image = image

    def can_swing(self, time):
        cooldown = self.bugnet_data["cooldown"] * 1000
        return (not self.swinging and not self.returning and time - self.last_swing_time >= cooldown)

    def swing(self, time):
        if self.can_swing(time):
            self.swinging = True
            self.returning = False
            self.swing_start_time = time
            self.last_swing_time = time

    def draw(self, screen, data, cursor_icon, cursor_icon_rect):
        if data["bugnet"] != self.current_bugnet:
            self.current_bugnet = data["bugnet"]
            self.bugnet_name = self.current_bugnet
            self.bugnet_data = self.bugnets_list[self.current_bugnet]

        current_time = pygame.time.get_ticks()

        if self.swinging:
            t = (current_time - self.swing_start_time) / (self.swing_duration * 1000)

            if t >= 1:
                t = 1
                self.swinging = False
                self.returning = True
                self.swing_start_time = current_time

            eased = math.sin(t * math.pi / 2)
            self.angle = eased * self.max_angle

        elif self.returning:
            t = (current_time - self.swing_start_time) / (self.return_duration * 1000)

            if t >= 1:
                t = 1
                self.returning = False
                self.angle = 0

            eased = 1 - math.cos(t * math.pi / 2)
            self.angle = (1 - eased) * self.max_angle

        mouseX, mouseY = pygame.mouse.get_pos()

        rotated_image = pygame.transform.rotate(self.original_image, self.angle)

        if self.visible:
            self.rect = rotated_image.get_rect(center=(mouseX, mouseY + 60))
            screen.blit(rotated_image, self.rect)
        else:
            cursor_icon_rect.center = (mouseX, mouseY)
            screen.blit(cursor_icon, cursor_icon_rect)