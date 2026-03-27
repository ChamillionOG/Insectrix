#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import pygame
import json

from environmentHandler import EnvironmentManager
from containerHandler import ContainerManager
from bugnetHandler import BugnetManager
from bugHandler import Bug, BugManager
from popupHandler import PopupText

#[------------]#
#[----DATA----]#
#[------------]#

from savesManager import load_game, save_game

default_data = {
    "bugs": 0,
    "max_bugs": 3,
    "spawn_rate": 5,
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
    "settings": {
        "sound_effects": True,
        "popups": True,
        "music": True
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

autosave_timer = 0
autosave_interval = 15000

popups = []
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

def font(name, size):
    return pygame.font.Font(f"assets/fonts/{name}.ttf", sx(size))

#[----------------]#
#[----MANAGERS----]#
#[----------------]#

environment_manager = EnvironmentManager((screen_width, screen_height), data)
container_manager = ContainerManager(data["container"]["type"], containers_list, screen, container_bugs, data)
bug_manager = BugManager(data["environment"], container_bugs, None, bugs_list, environments_list)
bugnet_manager = BugnetManager(data["bugnet"], bugnets_list)

#[---------------]#
#[----OPTIONS----]#
#[---------------]#

options_button = load_scaled("assets/ui/options_button.png", 70, 70)
options_button_rect = options_button.get_rect(topleft=scale_position(15, 15))

options_open = False
current_frame = None

stats_button = load_scaled("assets/ui/stats_button.png", 70, 70)
stats_rect = stats_button.get_rect(topleft=scale_position(15, 100))

settings_button = load_scaled("assets/ui/settings_button.png", 70, 70)
settings_rect = settings_button.get_rect(topleft=scale_position(15, 185))

quit_button = load_scaled("assets/ui/quit_button.png", 70, 70)
quit_rect = quit_button.get_rect(topleft=scale_position(15, 270))

options_frame = load_scaled("assets/ui/options_frame.png", 325, 475)
options_frame_rect = options_frame.get_rect(topleft=scale_position(95, 15))

def load_stats():
    title = font("ThinBold", 35).render("Stats", False, (255, 255, 255))
    max_bugs_text = font("Regular", 20).render(f"Max Bugs: {data["max_bugs"]}", True, (255, 255, 255))
    spawn_rate_text = font("Regular", 20).render(f"Spawn Rate: {data["spawn_rate"]}(s)", True, (255, 255, 255))
    bugnet_text = font("Regular", 20).render(f"Current Bugnet: {data["bugnet"]}", True, (255, 255, 255))
    environment_text = font("Regular", 20).render(f"Current Environment: {data["environment"]}", True, (255, 255, 255))
    sell_plan_text = font("Regular", 20).render(f"Current Sell Plan: {data["sell_plan"]}", True, (255, 255, 255))
    container_text = font("Regular", 20).render(f"Current Container: {data["container"]["type"]}", True, (255, 255, 255))
    capacity_text = font("Regular", 20).render(f"Max Capacity: {data["container"]["capacity"]}", True, (255, 255, 255))

    screen.blit(title, title.get_rect(center=scale_position(257.5, 80)))
    screen.blit(max_bugs_text, max_bugs_text.get_rect(center=scale_position(257.5, 120)))
    screen.blit(spawn_rate_text, spawn_rate_text.get_rect(center=scale_position(257.5, 150)))
    screen.blit(bugnet_text, bugnet_text.get_rect(center=scale_position(257.5, 180)))
    screen.blit(environment_text, environment_text.get_rect(center=scale_position(257.5, 210)))
    screen.blit(sell_plan_text, sell_plan_text.get_rect(center=scale_position(257.5, 240)))
    screen.blit(container_text, container_text.get_rect(center=scale_position(257.5, 270)))
    screen.blit(capacity_text, capacity_text.get_rect(center=scale_position(257.5, 300)))

def load_settings():
    title = font("ThinBold", 35).render("Settings", False, (255, 255, 255))

    if data["settings"]["sound_effects"]:
        sound_effects_button = font("Regular", 20).render("Sound Effects: ENABLED", True, (0, 255, 0))
    else:
        sound_effects_button = font("Regular", 20).render("Sound Effects: DISABLED", True, (255, 0, 0))

    if data["settings"]["popups"]:
        popups_button = font("Regular", 20).render("PopUps: ENABLED", True, (0, 255, 0))
    else:
        popups_button = font("Regular", 20).render("PopUps: DISABLED", True, (255, 0, 0))

    if data["settings"]["music"]:
        music_button = font("Regular", 20).render("Music: ENABLED", True, (0, 255, 0))
    else:
        music_button = font("Regular", 20).render("Music: DISABLED", True, (255, 0, 0))

    screen.blit(title, title.get_rect(center=scale_position(257.5, 80)))
    screen.blit(sound_effects_button, sound_effects_button.get_rect(center=scale_position(257.5, 130)))
    screen.blit(popups_button, popups_button.get_rect(center=scale_position(257.5, 170)))
    screen.blit(music_button, music_button.get_rect(center=scale_position(257.5, 210)))

#[---------------]#
#[----RUNNING----]#
#[---------------]#

running = True

container_manager.load_container(container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data)
bugnet_manager.load_bugnet(load_scaled)

current_container = data["container"]["type"]
current_bugnet = data["bugnet"]

static_surface = pygame.Surface((screen_width, screen_height))
static_surface.blit(environment_manager.image, (0, 0))

cursor_icon = load_scaled("assets/ui/mouse_cursor.png", 64, 64)
cursor_icon_rect = cursor_icon.get_rect()

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(data)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bug_manager.collect_bug(event.pos, pygame.time.get_ticks(), data, container_manager.rect, bugnet_manager, screen_bugs, popups, scale, font, PopupText)

            if options_button_rect.collidepoint(mouse_pos) and not options_open:
                options_open = True
            elif options_button_rect.collidepoint(mouse_pos) and options_open:
                options_open = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSLASH:
                data = default_data.copy()
                save_game(data)
                popups.append(PopupText((screen_width / 2, screen_height /2), "DATA WIPED", font("Regular", 50), (255, 0, 0)))

                container_manager.load_container(container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data)
                bugnet_manager.load_bugnet(load_scaled)

    dt = clock.tick(60) / 1000
    spawn_delay = base_spawn_delay * data["spawn_rate"]

    if len(screen_bugs) != data["max_bugs"]:
        spawn_timer += dt * 1000

    if spawn_timer >= spawn_delay and len(screen_bugs) < data["max_bugs"]:
        bug_manager.spawn_bug(screen_width, screen_height, screen_bugs, load_scaled)
        spawn_timer = 0

    autosave_timer += dt * 1000
    if autosave_timer >= autosave_interval:
        save_game(data)
        autosave_timer = 0

    for popup in popups[:]:
        popup.update(scale)
        if popup.dead():
            popups.remove(popup)

    new_container = data["container"]["type"]
    new_bugnet = data["bugnet"]

    if current_container != new_container:
        container_manager.load_container(container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data)
    elif current_bugnet != new_bugnet:
        bugnet_manager.load_bugnet(load_scaled)

    options_hovering = options_button_rect.collidepoint(mouse_pos)

    screen.blit(static_surface, (0, 0))
    screen.blit(container_manager.image, container_manager.rect)
    
    screen.blit(options_button, options_button_rect)

    bugnet_manager.draw(screen, data, cursor_icon, cursor_icon_rect)
    bug_manager.draw(screen_width, screen_bugs, screen, scale)
    container_manager.draw(container_bugs, screen, scale, screen_width)

    for popup in popups:
        popup.draw(screen)

    fps = clock.get_fps()
    fps_text = font("Regular", 20).render(f"FPS: {int(fps)}", False, (255, 255, 255))
    screen.blit(fps_text, scale_position(10, 10))
    screen.blit(options_frame, options_frame_rect)
    load_settings()

    if options_open:
        screen.blit(stats_button, stats_rect)
        screen.blit(settings_button, settings_rect)
        screen.blit(quit_button, quit_rect)
    
    if options_hovering:
        bugnet_manager.visible = False
    else:
        bugnet_manager.visible = True

    pygame.display.flip()