import pygame

from savesManager import save_data

class UpgradeButton:
    def __init__(self, x, y, width, height, frame_image, icon_image, name, price, font, effect=None):
        self.frame_image = pygame.transform.scale(frame_image, (width, height))
        self.rect = self.frame_image.get_rect(topleft=(x, y))
        self.icon_image = pygame.transform.scale(icon_image, (64, 64))
        self.name = name
        self.price = price
        self.font = font
        self.effect = effect

        self.name_text = font.render(name, True, (255, 255, 255))
        self.price_text = font.render(f"{price} Insectra", True, (240, 240, 240))

    def draw(self, screen):
        screen.blit(self.frame_image, self.rect)
        screen.blit(self.icon_image, (self.rect.x + 25, self.rect.y + 110))

        screen.blit(self.name_text, (self.rect.x + 100, self.rect.y + 110))
        screen.blit(self.price_text, (self.rect.x + 100, self.rect.y + 145))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def can_afford(self, data):
        return data["currency"] >= self.price
    
    def owns_upgrade(self, data):
        return data["purchases"].get(self.name, False)
    
    def apply_upgrade(self, data):
        if self.effect:
            self.effect(data)

class UpgradeManager:
    def __init__(self, margin_right, y, popup_manager, data, spacing=145):
        self.buttons = []
        self.margin_right = margin_right
        self.start_y = y
        self.popup_manager = popup_manager
        self.data = data
        self.spacing = spacing

    def add_button(self, button, screen_width):

        if not self.buttons:
            y = self.start_y
        else:
            last = self.buttons[-1]
            y = last.rect.top + self.spacing

        button.rect.topright = (screen_width - self.margin_right, y)

        self.buttons.append(button)

    def reorder_buttons(self, screen_width):
        y = self.start_y

        for button in self.buttons:
            button.rect.topright = (screen_width - self.margin_right, y)
            y += self.spacing

    def is_hovering(self, mouse_pos):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                return True
        return False

    def draw(self, screen):
        for button in reversed(self.buttons): # --- Displays buttons in order
            button.draw(screen)

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                
                if button.owns_upgrade(self.data): # --- If Owns Upgrade
                    self.popup_manager.spawn("Already Owned!", (255, 255, 255), button.rect.centerx - 275, button.rect.centery, 1)
                elif button.can_afford(self.data): # --- Purchased Upgrade
                    button.apply_upgrade(self.data)
                    self.popup_manager.spawn("Purchased!", (0, 255, 0), button.rect.centerx - 275, button.rect.centery, 1)
                    self.data["currency"] -= button.price
                    self.data["purchases"][button.name] = True
                    self.buttons.remove(button)
                    self.reorder_buttons(pygame.display.get_surface().get_width())
                    save_data(self.data)
                else: # --- Can't Afford Upgrade
                    self.popup_manager.spawn("Can't Afford.", (255, 0, 0), button.rect.centerx - 275, button.rect.centery, 1)

                return button
            
        return None