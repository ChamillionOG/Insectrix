import pygame
import random
import math

class Bug:
    def __init__(self, position, load_scaled, bug_data):
        self.x, self.y = position
        self.bug_data = bug_data

        self.key = self.bug_data["key"]
        self.name = self.bug_data["name"]
        self.image = load_scaled(self.bug_data["image"], 128, 128)
        self.amplitude = self.bug_data["amplitude"] # Higher = More Motion
        self.frequency = self.bug_data["frequency"] # Smaller = Closer Waves
        self.speed = self.bug_data["speed"]
        self.weight = self.bug_data["weight"]

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction = random.choice([-1, 1])
        self.base_y = self.y
        self.var = 0

        self.in_container = False
        self.targetY = None
        self.velX = random.uniform(-2.5, 2.5)
        self.velY = 0

    def draw(self, scale, screen, screen_width, container_rect=None):
        if not self.in_container:
            # Regular Side to Side Movement
            self.rect.x += self.direction * (self.speed * scale)

            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.direction *= -1

            self.var += 1
            self.rect.y = self.base_y + (int(self.amplitude * math.sin(self.frequency * self.var)) * scale)

            screen.blit(self.image, self.rect)
        else:
            # Container Physics
            gravity = 0.4 * scale
            air_resistance = 0.999
            bounce_damping = 0.4
            ground_friction = 0.85

            self.velY += gravity

            self.velX *= air_resistance
            self.velY *= air_resistance

            self.rect.x += self.velX
            self.rect.y += self.velY

            if self.rect.left <= container_rect.left:
                self.rect.left = container_rect.left
                self.velX *= -0.7

            if self.rect.right >= container_rect.right:
                self.rect.right = container_rect.right
                self.velX *= -0.7

            if self.targetY is not None and self.rect.bottom >= self.targetY:
                self.rect.bottom = self.targetY

                self.velY *= -bounce_damping
                self.velX *= ground_friction

                if abs(self.velY) < 0.3:
                    self.velY = 0

                if abs(self.velX) < 0.1:
                    self.velX = 0

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

    def spawn_bug(self, screen_width, screen_height, screen_bugs, load_scaled):
        bug_key = self.pick_bug()
        bug_data = self.bugs_list[bug_key]

        x = random.randint(128, screen_width - 128)
        y = random.randint(128, screen_height - 128)

        bug = Bug((x, y), load_scaled, bug_data)

        screen_bugs.append(bug)

    def collect_bug(self, pos, time, data, container_rect, bugnet_manager, screen_bugs, popups, scale, font, PopupText):
        if not bugnet_manager.can_swing(time):
            return False

        bugnet_manager.swing(time)

        for bug in screen_bugs[:]:
            if bug.rect.collidepoint(pos):
                if data["bugs"] < data["container"]["capacity"]:
                    screen_bugs.remove(bug)

                    bug.rect.midtop = (container_rect.centerx, container_rect.top + 20)
                    bug.in_container = True
                    bug.velY = 0
                    bug.velX = random.uniform(-2.5, 2.5)

                    self.container_bugs.append(bug)

                    capacity = data["container"]["capacity"]
                    inner_height = container_rect.height - (125 * scale)
                    spacing = inner_height / capacity

                    for i, b in enumerate(self.container_bugs):
                        b.targetY = container_rect.bottom - (i * spacing)

                    bugs = data["container"]["bugs"]
                    bugs[bug.key] = bugs.get(bug.key, 0) + 1

                    data["bugs"] += 1

                    popups.append(PopupText(pos, f"+1 {bug.name}", font("Regular", 30), (255, 255, 255)))

                    return True
                else:
                    popups.append(PopupText(pos, "Full Container!", font("Regular", 30), (255, 0, 0)))

        return False

    def draw(self, screen_width, screen_bugs, screen, scale):
        for bug in screen_bugs:
            bug.draw(scale, screen, screen_width)