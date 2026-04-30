import random
import math

class Bug:
    def __init__(self, position, load_scaled, bug_data):
        self.x, self.y = position
        self.bug_data = bug_data

        self.pos_x = float(self.x)
        self.pos_y = float(self.y)

        self.key = self.bug_data["key"]
        self.name = self.bug_data["name"]
        self.image = load_scaled(self.bug_data["image"], 128, 128)
        self.movement = self.bug_data["movement"]

        self.amplitude = self.bug_data["amplitude"]
        self.frequency = self.bug_data["frequency"]
        self.speed = self.bug_data["speed"]
        self.weight = self.bug_data["weight"]
        self.value = self.bug_data["value"]

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction = random.choice([-1, 1])
        self.base_y = self.y
        self.var = 0

        self.wander_angle = random.uniform(0, math.pi * 2)
        self.wander_strength = 2.5

        self.in_container = False
        self.targetY = None
        self.velX = random.uniform(-2.5, 2.5)
        self.velY = 0

    def draw(self, scale, screen, screen_width, sx, container_rect=None):
        if not self.in_container:
            if self.movement == "soft":
                self.pos_x += self.direction * (self.speed * scale)

                self.var += 1
                self.pos_y = self.base_y + (self.amplitude * math.sin(self.frequency * self.var)) * scale
            elif self.movement == "jittery":
                self.pos_x += self.direction * (self.speed * scale)

                self.wander_angle += random.uniform(-0.2, 0.2)

                wander_x = math.cos(self.wander_angle) * self.wander_strength
                wander_y = math.sin(self.wander_angle) * self.wander_strength

                self.pos_x += wander_x * scale
                self.pos_y += wander_y * scale

                if random.random() < 0.01:
                    self.direction *= -1

                self.var += 1
                drift = math.sin(self.frequency * self.var) * self.amplitude
                target_y = self.base_y + drift
                self.pos_y += (target_y - self.pos_y) * 0.05

            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)

            if self.rect.left <= sx(5):
                self.rect.left = sx(5)
                self.pos_x = self.rect.x
                self.direction = 1

            if self.rect.right >= screen_width - sx(5):
                self.rect.right = screen_width - sx(5)
                self.pos_x = self.rect.x
                self.direction = -1

        else:
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

    def collect_bug(self, pos, time, data, container_rect, bugnet_manager, screen_bugs, popups, scale, font, PopupText, ignore_cooldown=False):
        if not ignore_cooldown and not bugnet_manager.can_swing(time):
            return False

        if not ignore_cooldown:
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

                    popups.append(PopupText(pos, f"+1 {bug.name}", font("Regular", 30), (255, 255, 255), 40))

                    return True
                else:
                    popups.append(PopupText(pos, "Full Container!", font("Regular", 30), (255, 0, 0), 40))
        return False

    def draw(self, screen_width, screen_bugs, screen, scale, sx):
        for bug in screen_bugs:
            bug.draw(scale, screen, screen_width, sx)