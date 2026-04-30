import pygame
import random
import math

class BugCollector:
    def __init__(self, image, position):
        self.pos = pygame.Vector2(position)
        self.start_pos = pygame.Vector2(position)
        self.image = image

        self.target = None

        self.swinging = False
        self.returning = False
        self.swing_angle = 0
        self.idle_angle = 0
        self.final_angle = 0
        self.tilt_speed = random.uniform(0.0025, 0.01)

        self.max_swing_angle = 120
        self.swing_duration = 0.25
        self.return_duration = 0.2

        self.swing_start_time = 0

    def swing(self, current_time):
        if not self.swinging and not self.returning:
            self.swinging = True
            self.swing_start_time = current_time

    def choose_target(self, bugs):
        if bugs:
            self.target = random.choice(bugs)
        else:
            self.target = None

    def update(self, bugs, speed, data, collect_bug, container_rect, bugnet_manager, popups, scale, font, PopupText):
        if not data["settings"]["bug_catchers"]:
            direction = self.start_pos - self.pos
            distance = direction.length()

            if distance > 1:
                direction = direction.normalize()
                self.pos += direction * speed
            else:
                self.pos = self.start_pos.copy()
                
            self.target = None

            self.swinging = False
            self.returning = False

            self.swing_angle = 0
            self.idle_angle = 0
            self.final_angle = 0
            return

        current_time = pygame.time.get_ticks()

        if not self.swinging and not self.returning:
            self.idle_angle = 5 * math.cos(current_time * self.tilt_speed)
        else:
            self.idle_angle = 0

        if self.swinging:
            t = (current_time - self.swing_start_time) / (self.swing_duration * 1000)

            if t >= 1:
                t = 1
                self.swinging = False
                self.returning = True
                self.swing_start_time = current_time

            eased = math.sin(t * math.pi / 2)
            self.swing_angle = eased * self.max_swing_angle
        elif self.returning:
            t = (current_time - self.swing_start_time) / (self.return_duration * 1000)

            if t >= 1:
                t = 1
                self.returning = False
                self.swing_angle = 0

            eased = 1 - math.cos(t * math.pi / 2)
            self.swing_angle = (1 - eased) * self.max_swing_angle

        if self.target not in bugs:
            self.choose_target(bugs)

        if self.target:
            target_pos = pygame.Vector2(self.target.rect.center)
            direction = target_pos - self.pos
            distance = direction.length()

            if distance != 0:
                direction = direction.normalize()

            self.pos += direction * speed

            if distance < (50 * scale):
                center = self.target.rect.center

                collect_bug(center, current_time, data, container_rect, bugnet_manager, bugs, popups, scale, font, PopupText, True)

                self.swing(current_time)
                self.target = None

        else:
            direction = self.start_pos - self.pos
            distance = direction.length()

            if distance > 1:
                direction = direction.normalize()
                self.pos += direction * speed
            else:
                self.pos = self.start_pos.copy()
        
        self.final_angle = self.swing_angle + self.idle_angle

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.final_angle)
        rect = rotated.get_rect(center=self.pos)
        screen.blit(rotated, rect)