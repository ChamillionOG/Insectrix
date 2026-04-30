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

        if self.one_time:
            self.cost = self.base_cost
        elif self.data is not None and self.amount is not None:
            self.cost = int(self.base_cost * (1.15 ** data[self.amount]))
        else:
            self.cost = self.base_cost
        
        self.frame = load_scaled("assets/ui/upgrade_button_frame.png", 410.4, 125.6)
        self.cover = load_scaled("assets/ui/upgrade_cover_frame.png", 410.4, 125.6)

        self.name_text = font("ThinBold", 25).render(f"{self.name}", False, (255, 255, 255))
        self.cost_text = font("Thin", 20).render(f"{self.cost:,} Insectra", False, (255, 255, 255))

        self.rect = self.frame.get_rect(center=(self.x, self.y))

        self.visible = False

    def can_afford(self, data):
        return data["currency"] >= self.cost
    
    def owns_upgrade(self, data):
        return data["purchases"].get(self.name, False)

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
        return any(button.visible and button.rect.collidepoint(pos) for button in buttons)
    
    def update_cost(self, button, font, data):
        if button.one_time: return

        button.cost = int(button.base_cost * (1.15 ** data[button.amount]))
        button.cost_text = font("Thin", 20).render(f"{button.cost:,} Insectra", False, (255, 255, 255))

    def clicked(self, buttons, pos, data, scale, popups, font, PopupText):
        for button in buttons:
            if not button.visible: continue
            if button.clicked(pos):
                if button.can_afford(data):
                    popups.append(PopupText((button.rect.centerx - (325 * scale), button.rect.centery + (30 * scale)), "Purchased!", font("Regular", 30), (255, 255, 255), 40))
                    data["currency"] -= button.cost

                    if button.one_time:
                        data["purchases"][button.name] = True
                        buttons.remove(button)

                        if button.name == "Wooden Bugnet":
                            data["bugnet"] = "wooden"
                        elif button.name == "Sturdy Bugnet":
                            data["bugnet"] = "sturdy"
                        elif button.name == "Medium Jar":
                            data["container"]["type"] = "medium_jar"
                            data["container"]["capacity"] = 15
                            data["container"]["offset"] = 15
                            data["container"]["bugs"].clear()
                        elif button.name == "Basic Sell Plan":
                            data["sell_plan"] = "basic"
                        elif button.name == "Auto Sell":
                            data["owns_auto_sell"] = True
                        elif button.name == "Bionic Bugnet":
                            data[button.data] += 1
                    else:
                        data[button.amount] += 1
                        self.update_cost(button, font, data)

                        if button.name == "Pollen Bottle":
                            if data[button.data] > 0:
                                data[button.data] -= 0.05
                                data[button.data] = round(data[button.data], 2)
                        elif button.name == "Florescent Spray":
                            data[button.data] += 1
                        elif button.name == "Clockwork":
                            data[button.data] -= 100

                    self.organize_buttons(buttons)
                else:
                    popups.append(PopupText((button.rect.centerx - (325 * scale), button.rect.centery + (30 * scale)), "Can't Afford!", font("Regular", 30), (255, 0, 0), 40))

    def draw(self, buttons, screen, data, current_page):
        y = self.start_y

        for button in buttons:
            is_unique = button.one_time
            is_upgrade = not button.one_time

            button.visible = ((is_unique and current_page == "uniques" and not button.owns_upgrade(data)) or (is_upgrade and current_page == "upgrades"))

            if button.visible:
                button.rect.center = (self.position_x, y)
                button.draw(screen, data)
                y += self.padding