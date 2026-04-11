
class App:
    def __init__(self, name, padding, load_scaled):
        self.name = name
        self.image = load_scaled(f"assets/phone/{self.name}.png", 48, 48)
        self.rect = self.image.get_rect()

        self.padding_x, self.padding_y = padding

    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, phone_rect):
        self.rect.center = (phone_rect.left + self.padding_x, phone_rect.top + self.padding_y)
        screen.blit(self.image, self.rect)

class PhoneManager:
    def __init__(self, phone_status, load_scaled, scale_position):
        self.phone_off = load_scaled("assets/phone/phone_off.png", 300, 518.4)
        self.phone_on = load_scaled("assets/phone/phone_on.png", 300, 518.4)

        self.sell_frame_one = load_scaled("assets/phone/phone_sell1.png", 300, 518.4)
        self.sell_frame_two = load_scaled("assets/phone/phone_sell2.png", 300, 518.4)

        self.phone_status = phone_status

        self.off_position = scale_position(2400, 1880)
        self.on_position = scale_position(2400, 1480)

        self.image = self.phone_off
        self.rect = self.image.get_rect(midbottom=(self.off_position))

        self.target_y = self.rect.bottom

        self.apps = [
            App("sell_app", scale_position(80, 125), load_scaled)
        ]

        self.selling = False
        self.sell_timer = 0
        self.sell_duration = 0
        self.sell_frame = 0
    
    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)
    
    def clicked(self, pos, sellplans_list, data):
        if self.phone_status == "on":
            for app in self.apps:
                if app.is_hovering(pos):
                    if app.name == "sell_app" and data["bugs"] > 0:
                        plan_type = data["sell_plan"]
                        self.phone_status = "selling"
                        self.selling = True
                        self.sell_timer = 0
                        self.sell_frame = 0
                        self.sell_duration = sellplans_list[plan_type]["cooldown"]
                        self.image = self.sell_frame_one
                        self.sell_frame = 0
                    return

        if self.is_hovering(pos):
            if self.phone_status == "off":
                self.phone_status = "on"
                self.image = self.phone_on
                self.target_y = self.on_position[1]
            elif self.phone_status == "on":
                self.phone_status = "off"
                self.image = self.phone_off
                self.target_y = self.off_position[1]

    def draw(self, screen, dt, sy, data, container_manager, container_bugs, load_scaled, bugs_list, scale, Bug):
        speed = sy(20)

        if self.rect.bottom < self.target_y:
            self.rect.bottom += speed
            if self.rect.bottom > self.target_y:
                self.rect.bottom = self.target_y
        elif self.rect.bottom > self.target_y:
            self.rect.bottom -= speed
            if self.rect.bottom < self.target_y:
                self.rect.bottom = self.target_y

        if self.phone_status == "selling" and self.selling:
            self.sell_timer += dt
            self.sell_duration -= dt

            if self.sell_timer >= 0.5:
                self.sell_timer = 0
                self.sell_frame = 1 - self.sell_frame
                self.image = self.sell_frame_one if self.sell_frame == 0 else self.sell_frame_two
            
            if self.sell_duration <= 0:
                total = sum(data["container"]["bugs"].values())
                data["currency"] += total
                data["container"]["bugs"] = {}
                data["bugs"] = 0
                self.phone_status = "on"
                self.selling = False
                self.image = self.phone_on
                container_manager.load_bugs(container_bugs, load_scaled, bugs_list, scale, Bug, data)

        screen.blit(self.image, self.rect)

        if self.phone_status == "on":
            for app in self.apps:
                app.draw(screen, self.rect)