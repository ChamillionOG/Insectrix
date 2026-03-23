#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import pygame
import json

from environmentHandler import EnvironmentManager
from containerHandler import ContainerManager
from bugnetHandler import BugnetManager
from bugHandler import Bug, BugManager
from savesManager import load_game

#[------------]#
#[----DATA----]#
#[------------]#

default_data = {
    "bugs": 0,
    "max_bugs": 3,
    "spawn_rate": 1,
    "currency": 0,
    "bugnet": "wooden",
    "environment": "forest",
    "sellPlan": "free",
    "container": {
        "type": "small_jar",
        "capacity": 10,
        "offset": 15,
        "bugs": {}
    },
    "purchases": {}
}

data = load_game(default_data)

with open("dictionaries/bugDictionaries.json", "r") as f:
    bugs_list = json.load(f)

with open("dictionaries/bugnetDictionaries.json", "r") as f:
    bugnets_list = json.load(f)

with open("dictionaries/environmentDictionaries.json", "r") as f:
    environments_list = json.load(f)

with open("dictionaries/containerDictionaries.json", "r") as f:
    containers_list = json.load(f)

#[-----------------]#
#[----VARIABLES----]#
#[-----------------]#

spawn_timer = 0
base_spawn_delay = 1000

screen_bugs = []
container_bugs = []

clock = pygame.time.Clock()

#[-------------]#
#[----INIT-----]#
#[-------------]#

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Insectrix")
pygame.display.set_icon(pygame.image.load("assets/images/gameIcon.png"))

#[---------------]#
#[----DISPLAY----]#
#[---------------]#

BASE_WIDTH = 2560
BASE_HEIGHT = 1440

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
screen_width, screen_height = screen.get_size()

scale_x = screen_width / BASE_WIDTH
scale_y = screen_height / BASE_HEIGHT

scale = min(scale_x, scale_y)

def sx(x): return int(x * scale)
def sy(y): return int(y * scale)

def scale_position(x, y):
    return sx(x), sy(y)

def load_scaled(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (sx(width), sy(height)))

#[----------------]#
#[----MANAGERS----]#
#[----------------]#

environment_manager = EnvironmentManager((screen_width, screen_height), data)
container_manager = ContainerManager(data["container"]["type"], containers_list, screen, container_bugs, data)
bug_manager = BugManager(data["environment"], container_bugs, None, bugs_list, environments_list)
bugnet_manager = BugnetManager(data["bugnet"], bugnets_list)

#[---------------]#
#[----RUNNING----]#
#[---------------]#

running = True

container_manager.load_container(container_bugs, load_scaled, scale_position, data)
bugnet_manager.load_bugnet(load_scaled)

current_container = data["container"]["type"]
current_bugnet = data["bugnet"]

static_surface = pygame.Surface((screen_width, screen_height))
static_surface.blit(environment_manager.image, (0, 0))

cursor_icon = load_scaled("assets/ui/mouse_cursor.png", 64, 64)
cursor_icon_rect = cursor_icon.get_rect()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bug_manager.collect_bug(event.pos, pygame.time.get_ticks(), data, container_manager.rect, bugnet_manager, screen_bugs)

    dt = clock.tick(60) / 1000

    spawn_delay = base_spawn_delay / data["spawn_rate"]
    spawn_timer += dt * 1000

    if spawn_timer >= spawn_delay and len(screen_bugs) < data["max_bugs"]:
        bug_manager.spawn_bug(screen_width, screen_height, screen_bugs, load_scaled)
        spawn_timer = 0

    new_container = data["container"]["type"]
    new_bugnet = data["bugnet"]

    if current_container != new_container:
        container_manager.load_container(container_bugs, load_scaled, scale_position, data)
    elif current_bugnet != new_bugnet:
        bugnet_manager.load_bugnet(load_scaled)

    screen.blit(static_surface, (0, 0))
    screen.blit(container_manager.image, container_manager.rect)

    bugnet_manager.draw(screen, data, cursor_icon, cursor_icon_rect)
    bug_manager.draw(screen_width, screen_bugs, screen)

    pygame.display.flip()