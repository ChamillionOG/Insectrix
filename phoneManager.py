import pygame
import time

from savesManager import load_data, save_data
from containerManager import ContainerManager
from dictionaries.sellDictionaries import sell_dictionaries

class AppIcon:
    def __init__(self, name, image_path, offset_x, offset_y, size=(48, 48)):
        self.name = name
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.rect = self.image.get_rect()

    def updatePosition(self, phone_rect):
        self.rect.topleft = (phone_rect.left + self.offset_x, phone_rect.top + self.offset_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class PhoneManager:
    def __init__(self, screen_width, screen_height, container_manager, data, status="off"):
        self.phone_off = pygame.image.load("assets/phone/phone_off.png").convert_alpha()
        self.phone_off = pygame.transform.scale(self.phone_off, (275, 500))

        self.phone_on = pygame.image.load("assets/phone/phone_on.png").convert_alpha()
        self.phone_on = pygame.transform.scale(self.phone_on, (275, 500))

        self.phone_sell1 = pygame.image.load("assets/phone/phone_sell1.png").convert_alpha()
        self.phone_sell1 = pygame.transform.scale(self.phone_sell1, (275, 500))

        self.phone_sell2 = pygame.image.load("assets/phone/phone_sell2.png").convert_alpha()
        self.phone_sell2 = pygame.transform.scale(self.phone_sell2, (275, 500))

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.container_manager = container_manager
        self.data = data
        self.status = status

        self.image = self.phone_off
        self.rect = self.image.get_rect(bottomright=(screen_width, screen_height + 400))
        self.speed = 1000
        self.offY = screen_height + 400
        self.onY = screen_height
        self.targetY = self.offY

        self.apps = [
            AppIcon("sellApp", "assets/phone/sell_app.png", 40, 80),
        ]

        self.selling = False
        self.sell_timer = 0
        self.sell_duration = 0
        self.sell_frame = 0

    def updatePhoneStatus(self, statusInput):
        self.status = statusInput

    def is_hovering(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def handle_click(self, mouse_pos, data):
        if self.status == "on":
            for app in self.apps:
                if app.handle_click(mouse_pos):
                    if app.name == "sellApp" and self.data["bugs"] > 0:
                        plan_type = data["sellPlan"]
                        self.status = "selling"
                        self.selling = True
                        self.sell_timer = 0
                        self.sell_frame = 0
                        self.sell_duration = sell_dictionaries[plan_type]["cooldown"]
                        self.image = self.phone_sell1
                        self.sell_frame = 0
                    return
                
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

        if self.status == "selling" and self.selling:
            self.sell_timer += dt
            self.sell_duration -= dt

            if self.sell_timer >= 0.5:
                self.sell_timer = 0
                self.sell_frame = 1 - self.sell_frame
                self.image = self.phone_sell1 if self.sell_frame == 0 else self.phone_sell2

            if self.sell_duration <= 0:
                total = sum(self.data["container"]["bugs"].values())
                self.data["currency"] += total
                self.data["container"]["bugs"] = {}
                self.data["bugs"] = 0
                save_data(self.data)
                self.container_manager.refreshBugs()
                self.status = "on"
                self.selling = False
                self.image = self.phone_on
        
        screen.blit(self.image, self.rect)

        if self.status == "on":
            for app in self.apps:
                app.updatePosition(self.rect)
                app.draw(screen)