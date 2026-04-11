class PhoneManager:
    def __init__(self, phone_status, load_scaled, scale_position):
        self.phone_off = load_scaled("assets/phone/phone_off.png", 300, 518.4)
        self.phone_on = load_scaled("assets/phone/phone_on.png", 300, 518.4)

        self.phone_status = phone_status

        self.off_position = scale_position(2400, 1880)
        self.on_position = scale_position(2400, 1480)

        self.image = self.phone_off
        self.rect = self.image.get_rect(midbottom=(self.off_position))

        self.target_y = self.rect.bottom
    
    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)
    
    def clicked(self, pos):
        if self.is_hovering(pos):
            if self.phone_status == "off":
                self.phone_status = "on"
                self.image = self.phone_on
                self.target_y = self.on_position[1]
            elif self.phone_status == "on":
                self.phone_status = "off"
                self.image = self.phone_off
                self.target_y = self.off_position[1]

    def draw(self, screen, sy):
        speed = sy(20)

        if self.rect.bottom < self.target_y:
            self.rect.bottom += speed
            if self.rect.bottom > self.target_y:
                self.rect.bottom = self.target_y
        elif self.rect.bottom > self.target_y:
            self.rect.bottom -= speed
            if self.rect.bottom < self.target_y:
                self.rect.bottom = self.target_y

        screen.blit(self.image, self.rect)