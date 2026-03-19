import pygame

class BugnetManager:
    def __init__(self, current_bugnet, bugnets_list):
        self.current_bugnet = current_bugnet
        self.bugnets_list = bugnets_list

        self.swinging = False
        self.returning = False
        self.visible = True

        self.angle = 0
        self.max_angle = 80
        self.swing_speed = 24
        self.last_swing_time = 0

        self.bugnet_name = self.current_bugnet
        self.bugnet_data = self.bugnets_list[self.current_bugnet]

        self.load_bugnet()

    def load_bugnet(self):
        image = pygame.image.load(f"assets/images/bugnets/{self.bugnet_name}.png").convert_alpha()
        image = pygame.transform.scale(image, (256, 256))

        self.original_image = image
        self.image = image

    def can_swing(self, time):
        current_time = time
        cooldown = self.bugnet_data["cooldown"] * 1000

        return(not self.swinging and not self.returning and current_time - self.last_swing_time >= cooldown)
    
    def swing(self, time):
        if self.can_swing(time):
            self.swinging = True
            self.last_swing_time = time

    def draw(self, screen, data, cursor_icon, cursor_icon_rect):
        if data["bugnet"] != self.current_bugnet:
            self.current_bugnet = data["bugnet"]
            self.bugnet_name = self.current_bugnet
            self.bugnet_data = self.bugnets_list[self.current_bugnet]
            self.load_bugnet()

        if self.swinging:
            self.angle += self.swing_speed

            if self.angle >= self.max_angle:
                self.angle = self.max_angle
                self.swinging = False
                self.returning = True
        elif self.returning:
            self.angle -= self.swing_speed

            if self.angle <= 0:
                self.returning = False
                self.angle = 0

        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = rotated_image.get_rect()

        mouseX, mouseY = pygame.mouse.get_pos()

        self.rect = self.image.get_rect()

        if self.visible:
            self.rect.centerx = mouseX
            self.rect.centery = mouseY + 60

            screen.blit(rotated_image, self.rect)
        else:
            cursor_icon_rect.centerx = mouseX
            cursor_icon_rect.centery = mouseY

            screen.blit(cursor_icon, cursor_icon_rect)