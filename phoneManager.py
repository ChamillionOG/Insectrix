import pygame

class PhoneManager():
    def __init__(self, screen_width, screen_height, status="off"):
        self.phone_off = pygame.image.load("assets/phone/phone_off.png").convert_alpha()
        self.phone_off = pygame.transform.scale(self.phone_off, (275, 500))

        self.phone_on = pygame.image.load("assets/phone/phone_on.png").convert_alpha()
        self.phone_on = pygame.transform.scale(self.phone_on, (275, 500))

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.status = status

        self.image = self.phone_off
        self.rect = self.image.get_rect(bottomright=(screen_width, screen_height + 400))
        self.speed = 1000
        self.offY = screen_height + 400
        self.onY = screen_height
        self.targetY = self.offY

    def updatePhoneStatus(self, statusInput):
        self.status = statusInput

    def is_hovering(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.status == "off":
                self.status = "on"
                self.targetY = self.onY
            elif self.status == "on":
                self.status = "off"
                self.targetY = self.offY

    def update(self, screen, dt):
        if self.status == "off":
            self.image = self.phone_off
        elif self.status == "on":
            self.image = self.phone_on

        currentY = self.rect.bottom
        distance = self.targetY - currentY

        if abs(distance) > 1:
            move = self.speed * dt

            if distance > 0:
                currentY += min(move, distance)
            else:
                currentY -= min(move, -distance)

            self.rect.bottom = currentY

        self.rect.right = self.screen_width
        screen.blit(self.image, self.rect)