import pygame

class UpgradeButton:
    def __init__(self, rect, title, base_cost, cost, icon, save_key):
        self.rect = rect
        
        self.title = title
        self.base_cost = base_cost
        self.cost = cost
        self.icon = icon
        self.save_key = save_key

    def can_afford(self, data):
        return data["currency"] >= self.cost
    
    def click(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
    def purchase(self, data):
        pass

    def draw(self, screen, text_title, text_price, data):
        can_afford = False

        padding = 10

        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.topleft = (self.rect.left + padding, self.rect.top + padding)
            screen.blit(self.icon, icon_rect)

        title = text_title.render(self.title, False, (255, 255, 255))
        screen.blit(title, (self.rect.left + 70, self.rect.top + 10))

        cost = text_price.render(f"{self.cost:,} Currency", False, (255, 255, 255))
        screen.blit(cost, (self.rect.left + 70, self.rect.top + 40))