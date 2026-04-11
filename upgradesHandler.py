import pygame

class UpgradeButton:
    def __init__(self, position, config, load_scaled, font, scale, data):
        self.x, self.y = position
        self.config = config
        self.scale = scale

        self.name = self.config["name"]
        self.icon = load_scaled(self.config["icon"], 78, 78)
        self.base_cost = self.config["cost"]
        self.data = self.config["data"]
        self.amount = self.config["amount"]
        self.one_time = self.config["one_time"]

        self.cost = int(self.base_cost * (1.15 ** data[self.amount]))
        
        self.frame = load_scaled("assets/ui/upgrade_button_frame.png", 410.4, 125.6)
        self.cover = load_scaled("assets/ui/upgrade_cover_frame.png", 410.4, 125.6)

        self.name_text = font("ThinBold", 25).render(f"{self.name}", False, (255, 255, 255))
        self.cost_text = font("Thin", 20).render(f"{self.cost} Insectra", False, (255, 255, 255))

        self.rect = self.frame.get_rect(center=(self.x, self.y))

    def can_afford(self, data):
        return data["currency"] >= self.cost

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, data):
        screen.blit(self.frame, self.rect)

        if not self.can_afford(data):
            screen.blit(self.cover, self.rect)
        
        icon_rect = self.icon.get_rect(center=(self.rect.centerx - (155 * self.scale), self.rect.centery + (13 * self.scale)))
        screen.blit(self.icon, icon_rect)

        name_rect = self.name_text.get_rect(midleft=(self.rect.centerx - (120 * self.scale), self.rect.centery + (2 * self.scale)))
        screen.blit(self.name_text, name_rect)

        cost_rect = self.cost_text.get_rect(midleft=(self.rect.centerx - (120 * self.scale), self.rect.centery + (32 * self.scale)))
        screen.blit(self.cost_text, cost_rect)

class UpgradeManager:
    def __init__(self, start_y, position_x, padding):
        self.start_y = start_y
        self.position_x = position_x
        self.padding = padding

    def create_button(self, button, buttons):
        if not buttons:
            y = self.start_y
        else:
            last = buttons[-1]
            y = last.rect.centery + self.padding
        
        button.rect.center = (self.position_x, y)

        buttons.append(button)
    
    def organize_buttons(self, buttons):
        y = self.start_y

        for button in buttons:
            button.rect.center = self.position_x, y
            y += self.padding
    
    def is_hovering(self, buttons, pos):
        return any(button.rect.collidepoint(pos) for button in buttons)
    
    def update_cost(self, button, font, data):
        button.cost = int(button.base_cost * (1.15 ** data[button.amount]))
        button.cost_text = font("Thin", 20).render(f"{button.cost} Insectra", False, (255, 255, 255))

    def clicked(self, buttons, pos, data, scale, popups, font, PopupText):
        for button in buttons:
            if button.clicked(pos):
                if button.can_afford(data):
                    popups.append(PopupText((button.rect.centerx - (325 * scale), button.rect.centery + (30 * scale)), "Purchased!", font("Regular", 30), (255, 255, 255)))
                    data["currency"] -= button.cost

                    if button.one_time:
                        data["purchases"][button.name] = True
                        buttons.remove(button)
                    else:
                        data[button.amount] += 1
                        self.update_cost(button, font, data)

                        if button.name == "Pollen Bottle":
                            if data[button.data] > 0:
                                data[button.data] -= 0.01
                        elif button.name == "Florescent Spray":
                            data[button.data] += 1

                    self.organize_buttons(buttons)
                else:
                    popups.append(PopupText((button.rect.centerx - (325 * scale), button.rect.centery + (30 * scale)), "Can't Afford!", font("Regular", 30), (255, 0, 0)))

    def draw(self, buttons, screen, data):
        for button in reversed(buttons):
            button.draw(screen, data)