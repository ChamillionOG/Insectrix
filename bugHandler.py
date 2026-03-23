import pygame
import random
import math

class Bug:
    def __init__(self, position, bug_data):
        self.x, self.y = position
        self.bug_data = bug_data

        self.name = self.bug_data["name"]
        self.image = pygame.image.load(self.bug_data["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.amplitude = self.bug_data["amplitude"]
        self.frequency = self.bug_data["frequency"]
        self.speed = self.bug_data["speed"]
        self.weight = self.bug_data["weight"]

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction = random.choice([-1, 1])
        self.base_y = self.y
        self.var = 0

        self.velX = random.uniform(-2.5, 2.5)
        self.velY = 0

    def draw(self, screen, screen_width):
        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1

        self.var += 1
        self.rect.y = self.base_y + int(self.amplitude * math.sin(self.frequency * self.var))

        screen.blit(self.image, self.rect)
    
class BugManager:
    def __init__(self, current_environment, container_bugs, popup_manager, bugs_list, enviroments_list):
        self.current_environment = current_environment
        self.container_bugs = container_bugs
        self.popup_manager = popup_manager
        self.bugs_list = bugs_list
        self.environments_list = enviroments_list

        self.previous_environment = current_environment

    def clear_bugs(self, screen_bugs):
        if self.current_environment != self.previous_environment:
            screen_bugs.clear()
            self.previous_environment = self.current_environment

    def pick_bug(self):
        env = self.environments_list[self.current_environment]

        bug_keys = env["bugs"]
        weights = [self.bugs_list[key]["weight"] for key in bug_keys]

        return random.choices(bug_keys, weights=weights, k=1)[0]

    def spawn_bug(self, screen_width, screen_height, screen_bugs):
        bug_key = self.pick_bug()

        bug_data = self.bugs_list[bug_key]

        x = random.randint(0, screen_width - 128)
        y = random.randint(0, screen_height - 128)

        bug = Bug((x, y), bug_data)

        screen_bugs.append(bug)

    def collect_bug(self, pos, time, data, container_rect, bugnet_manager, popup_manager):
        if not bugnet_manager.can_swing(time):
            return False
        
        mouseX, mouseY = pygame.mouse.get_pos()

        for bug in self.screen_bugs:
            if bug.rect.collidepoint(pos):
                if data["bugs"] < data["container"]["capacity"]:
                    self.screen_bugs.remove(bug)
                    bug.rect.midtop = (container_rect.centerx, container_rect.top + 20)

                    self.container_bugs.append(bug)

                    bugs = data["container"]["bugs"]
                    bugs[bug.name] = bugs.get(bug.name, 0) + 1
                    bug_name = bug.name

                    data["bugs"] += 1

                    return True
                elif data["bugs"] == data["container"]["capacity"]:
                    #popup
                    pass

    def draw(self, screen_width, screen_bugs, screen):
        for bug in screen_bugs:
            bug.draw(screen, screen_width)