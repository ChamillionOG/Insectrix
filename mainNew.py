#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import pygame
import json

from environmentHandler import EnvironmentManager
from containerHandler import ContainerManager
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
pygame.mouse.set_visible(True)
pygame.display.set_caption("Insectrix")
pygame.display.set_icon(pygame.image.load("assets/images/gameIcon.png"))

#[---------------]#
#[----DISPLAY----]#
#[---------------]#

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
screen_width, screen_height = screen.get_size()

#[----------------]#
#[----MANAGERS----]#
#[----------------]#

environment_manager = EnvironmentManager((screen_width, screen_height), data)
container_manager = ContainerManager(data["container"]["type"], containers_list, screen, container_bugs, data)
bug_manager = BugManager(data["environment"], container_bugs, None, bugs_list, environments_list)

#[---------------]#
#[----RUNNING----]#
#[---------------]#

running = True

container_manager.load_container(container_bugs, data)

static_surface = pygame.Surface((screen_width, screen_height))
static_surface.blit(environment_manager.image, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    spawn_delay = base_spawn_delay / data["spawn_rate"]
    spawn_timer += dt * 1000

    if spawn_timer >= spawn_delay and len(screen_bugs) < data["max_bugs"]:
        bug_manager.spawn_bug(screen_width, screen_height, screen_bugs)
        spawn_timer = 0

    screen.blit(static_surface, (0, 0))
    screen.blit(container_manager.image, container_manager.rect)

    bug_manager.draw(screen_width, screen_bugs, screen)

    pygame.display.flip()