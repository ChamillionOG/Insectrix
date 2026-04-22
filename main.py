#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import webbrowser
import pygame
import json
import math
import sys

from upgradesHandler import UpgradeButton, UpgradeManager
from environmentHandler import EnvironmentManager
from containerHandler import ContainerManager
from bugnetHandler import BugnetManager
from bugHandler import Bug, BugManager
from phoneHandler import PhoneManager
from popupHandler import PopupText

#[------------]#
#[----DATA----]#
#[------------]#

from savesManager import load_game, save_game

default_data = {
    "bugs": 0,
    "max_bugs": 1,
    "spawn_rate": 5,
    "currency": 0,
    "bugnet": "wooden",
    "environment": "forest",
    "sprays_bought": 0,
    "pollen_bought": 0,
    "clocks_bought": 0,
    "sell_plan": "free",
    "owns_auto_sell": False,
    "auto_sell_interval": 15000,
    "container": {
        "type": "small_jar",
        "capacity": 10,
        "offset": 15,
        "bugs": {}
    },
    "settings": {
        "sound_effects": True,
        "popups": True,
        "music": True,
        "fps": False,
        "auto_sell": False,
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

with open("dictionaries/upgradeDictionaries.json", "r") as f:
    upgrades_list = json.load(f)

with open("dictionaries/sellDictionaries.json", "r") as f:
    sellplans_list = json.load(f)

#[-----------------]#
#[----VARIABLES----]#
#[-----------------]#

spawn_timer = 0
base_spawn_delay = 1000

autosave_timer = 0
autosave_interval = 5000 # ms

auto_sell_timer = 0

popups = []
screen_bugs = []
container_bugs = []
upgrade_buttons = []

clock = pygame.time.Clock()
display_currency = data["currency"]

#[-------------]#
#[----INIT-----]#
#[-------------]#

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Insectrix")
pygame.display.set_icon(pygame.image.load("assets/images/gameIcon.png"))

def update_button(button_img, scale, hovered, center, scale_speed=0.3, hover_scale=1.08, base_scale=1.0):
    target = base_scale * (hover_scale if hovered else 1.0)
    scale += (target - scale) * scale_speed

    new_width = max(1, int(button_img.get_width() * scale))
    new_height = max(1, int(button_img.get_height() * scale))

    scaled_img = pygame.transform.scale(button_img, (new_width, new_height))
    new_rect = scaled_img.get_rect(center=center)

    return scaled_img, new_rect, scale

def main_menu(screen, screen_width, screen_height, cursor_icon, cursor_icon_rect, sx, sy, load_scaled):
    title_x = screen_width // 2
    title_size = 1

    sky_x = 0
    sky_speed = sx(2)

    title = load_scaled("assets/ui/insectrix_banner.png", 1680, 508)
    overlay = load_scaled("assets/ui/forest_front.png", 2560, 1440)
    sky = load_scaled("assets/ui/forest_back.png", 5120, 1440)

    sky_width = sky.get_width()

    play_button = load_scaled("assets/ui/play_button.png", 336, 96)
    play_button_rect = play_button.get_rect(center=(title_x, sy(800)))
    play_scale = 1

    credits_button = load_scaled("assets/ui/credits_button.png", 336, 96)
    credits_button_rect = credits_button.get_rect(center=(title_x, sy(925)))
    credits_scale = 0
    credits_open = False

    credits_frame = load_scaled("assets/ui/options_frame.png", 756, 1140)
    credits_frame_x = screen_width + sx(200)
    credits_frame_size = 1
    credits_frame_rect = credits_frame.get_rect(center=(credits_frame_x, screen_height // 2))

    quit_button = load_scaled("assets/ui/quit_button_main.png", 336, 96)
    quit_button_rect = quit_button.get_rect(center=(title_x, sy(1050)))
    quit_scale = 1

    social_button_y = sy(1125)

    x_button = load_scaled("assets/ui/x_icon.png", 135, 105)
    x_button_rect = x_button.get_rect(center=(credits_frame_x - sx(160), social_button_y))
    x_scale = 1

    discord_button = load_scaled("assets/ui/discord_icon.png", 135, 105)
    discord_button_rect = discord_button.get_rect(center=(credits_frame_x - sx(50), social_button_y))
    discord_scale = 1

    cashapp_button = load_scaled("assets/ui/cashapp_icon.png", 135, 105)
    cashapp_button_rect = cashapp_button.get_rect(center=(credits_frame_x + sx(60), social_button_y))
    cashapp_scale = 1

    venmo_button = load_scaled("assets/ui/venmo_icon.png", 135, 105)
    venmo_button_rect = venmo_button.get_rect(center=(credits_frame_x + sx(160), social_button_y))
    venmo_scale = 1

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        time_sec = current_time / 1000

        sky_x -= sky_speed
        if sky_x <= -sky_width:
            sky_x = 0

        screen.blit(sky, (sky_x, 0))
        screen.blit(sky, (sky_x + sky_width, 0))
        screen.blit(overlay, overlay.get_rect(center=(screen_width // 2, screen_height // 2)))

        if credits_open:
            target_title_x = screen_width // 3.5
            target_title_size = 0.75
            target_credits_frame_x = screen_width // 1.3
            target_credits_size = 1
        else:
            target_title_x = screen_width // 2
            target_title_size = 1
            target_credits_frame_x = screen_width + sx(250)
            target_credits_size = 0

        title_x += (target_title_x - title_x) * 0.08
        title_size += (target_title_size - title_size) * 0.08
        credits_frame_x += (target_credits_frame_x - credits_frame_x) * 0.12
        credits_frame_size += (target_credits_size - credits_frame_size) * 0.2

        credits_content_scale = max(0.0, min(1.0, credits_frame_size))
        frame_center_y = screen_height // 2
        frame_center = (credits_frame_x, frame_center_y)

        title_tilt = 1.5 * math.cos(time_sec * 1.2)
        title_scale = title_size + 0.015 * math.sin(time_sec * 1.2)

        animated_title = pygame.transform.rotozoom(title, title_tilt, title_scale)
        title_rect = animated_title.get_rect(center=(title_x, sy(300)))
        screen.blit(animated_title, title_rect)

        scaled_frame = pygame.transform.rotozoom(credits_frame, 0, credits_frame_size)
        credits_frame_rect = scaled_frame.get_rect(center=(credits_frame_x, screen_height // 2))
        screen.blit(scaled_frame, credits_frame_rect)

        if credits_content_scale > 0.02:
            credits_label = font("ThinBold", max(1, int(75 * credits_content_scale))).render("Credits", True, (255, 255, 255))
            developer_label = font("Regular", max(1, int(40 * credits_content_scale))).render("Created Entirely By:", True, (255, 255, 255))
            developer_name = font("Regular", max(1, int(40 * credits_content_scale))).render("ChamillionDevs", True, (255, 255, 255))
            socials_label = font("ThinBold", max(1, int(60 * credits_content_scale))).render("Socials", True, (255, 255, 255))

            screen.blit(credits_label, credits_label.get_rect(center=(frame_center[0], frame_center_y - sy(420) * credits_content_scale)))
            screen.blit(developer_label, developer_label.get_rect(center=(frame_center[0], frame_center_y - sy(300) * credits_content_scale)))
            screen.blit(developer_name, developer_name.get_rect(center=(frame_center[0], frame_center_y - sy(230) * credits_content_scale)))
            screen.blit(socials_label, socials_label.get_rect(center=(frame_center[0], frame_center_y + sy(280) * credits_content_scale)))

        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        x_center = (credits_frame_x - sx(160) * credits_content_scale, frame_center_y + sy(405) * credits_content_scale)
        discord_center = (credits_frame_x - sx(50) * credits_content_scale, frame_center_y + sy(405) * credits_content_scale)
        cashapp_center = (credits_frame_x + sx(60) * credits_content_scale, frame_center_y + sy(405) * credits_content_scale)
        venmo_center = (credits_frame_x + sx(160) * credits_content_scale, frame_center_y + sy(405) * credits_content_scale)

        scaled_x_button, x_button_rect, x_scale = update_button(x_button, x_scale, x_button_rect.collidepoint(mouse_pos), x_center, base_scale=credits_content_scale)
        scaled_discord_button, discord_button_rect, discord_scale = update_button(discord_button, discord_scale, discord_button_rect.collidepoint(mouse_pos), discord_center, base_scale=credits_content_scale)
        scaled_cashapp_button, cashapp_button_rect, cashapp_scale = update_button(cashapp_button, cashapp_scale, cashapp_button_rect.collidepoint(mouse_pos), cashapp_center, base_scale=credits_content_scale)
        scaled_venmo_button, venmo_button_rect, venmo_scale = update_button(venmo_button, venmo_scale, venmo_button_rect.collidepoint(mouse_pos), venmo_center, base_scale=credits_content_scale)

        if credits_content_scale > 0.02:
            screen.blit(scaled_x_button, x_button_rect)
            screen.blit(scaled_discord_button, discord_button_rect)
            screen.blit(scaled_cashapp_button, cashapp_button_rect)
            screen.blit(scaled_venmo_button, venmo_button_rect)

        scaled_play_button, play_button_rect, play_scale = update_button(play_button, play_scale, play_button_rect.collidepoint(mouse_pos), (title_x, sy(800)))
        scaled_credits_button, credits_button_rect, credits_scale = update_button(credits_button, credits_scale, credits_button_rect.collidepoint(mouse_pos), (title_x, sy(925)))
        scaled_quit_button, quit_button_rect, quit_scale = update_button(quit_button, quit_scale, quit_button_rect.collidepoint(mouse_pos), (title_x, sy(1050)))

        screen.blit(scaled_play_button, play_button_rect)
        screen.blit(scaled_credits_button, credits_button_rect)
        screen.blit(scaled_quit_button, quit_button_rect)

        cursor_icon_rect.center = (mouse_x + sx(10), mouse_y + sy(10))
        screen.blit(cursor_icon, cursor_icon_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    return
                if credits_button_rect.collidepoint(event.pos):
                    credits_open = not credits_open
                if quit_button_rect.collidepoint(event.pos):
                    sys.exit()

                if x_button_rect.collidepoint(event.pos):
                    webbrowser.open_new_tab("https://x.com/ChamillionOG")
                elif discord_button_rect.collidepoint(event.pos):
                    webbrowser.open_new_tab("https://discordapp.com/users/829037484515000380")
                elif cashapp_button_rect.collidepoint(event.pos):
                    webbrowser.open_new_tab("https://cash.app/$EmilianHasa")
                elif venmo_button_rect.collidepoint(event.pos):
                    webbrowser.open_new_tab("https://www.venmo.com/u/Emilian-Hasa")

        pygame.display.flip()

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

cursor_icon = load_scaled("assets/ui/mouse_cursor.png", 48, 48)
cursor_icon_rect = cursor_icon.get_rect()

main_menu(screen, screen_width, screen_height, cursor_icon, cursor_icon_rect, sx, sy, load_scaled)

last_currency = None
currency_text_scale = 1.0

#[----------------]#
#[----MANAGERS----]#
#[----------------]#

environment_manager = EnvironmentManager((screen_width, screen_height), data)
container_manager = ContainerManager(data["container"]["type"], containers_list, screen)
bug_manager = BugManager(data["environment"], container_bugs, None, bugs_list, environments_list)
bugnet_manager = BugnetManager(data["bugnet"], bugnets_list)
upgrade_manager = UpgradeManager(sy(63), sx(2335), sy(123))
phone_manager = PhoneManager("off", load_scaled, scale_position)

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
    max_bugs_text = font("Regular", 18).render(f"Max Bugs: {data["max_bugs"]}", True, (255, 255, 255))
    spawn_rate_text = font("Regular", 18).render(f"Spawn Rate: {data["spawn_rate"]} (s)", True, (255, 255, 255))
    sell_interval_text = font("Regular", 18).render(f"Auto Sell Interval: {data["auto_sell_interval"] / 1000} (s)", True, (255, 255, 255))
    bugnet_text = font("Regular", 18).render(f"Current Bugnet: {data["bugnet"]}", True, (255, 255, 255))
    environment_text = font("Regular", 18).render(f"Current Environment: {data["environment"]}", True, (255, 255, 255))
    sell_plan_text = font("Regular", 18).render(f"Current Sell Plan: {data["sell_plan"]}", True, (255, 255, 255))
    container_text = font("Regular", 18).render(f"Current Container: {data["container"]["type"]}", True, (255, 255, 255))
    capacity_text = font("Regular", 18).render(f"Max Capacity: {data["container"]["capacity"]}", True, (255, 255, 255))

    screen.blit(title, title.get_rect(center=scale_position(257.5, 80)))
    screen.blit(max_bugs_text, max_bugs_text.get_rect(center=scale_position(257.5, 120)))
    screen.blit(spawn_rate_text, spawn_rate_text.get_rect(center=scale_position(257.5, 150)))
    screen.blit(sell_interval_text, sell_interval_text.get_rect(center=scale_position(257.5, 180)))
    screen.blit(bugnet_text, bugnet_text.get_rect(center=scale_position(257.5, 210)))
    screen.blit(environment_text, environment_text.get_rect(center=scale_position(257.5, 240)))
    screen.blit(sell_plan_text, sell_plan_text.get_rect(center=scale_position(257.5, 270)))
    screen.blit(container_text, container_text.get_rect(center=scale_position(257.5, 300)))
    screen.blit(capacity_text, capacity_text.get_rect(center=scale_position(257.5, 330)))

def load_settings():
    title = font("ThinBold", 35).render("Settings", False, (255, 255, 255))
    owns_sell_plan = data["owns_auto_sell"]

    if data["settings"]["sound_effects"]:
        sound_effects_button = font("Regular", 18).render("Sound Effects: ENABLED", True, (0, 255, 0))
    else:
        sound_effects_button = font("Regular", 18).render("Sound Effects: DISABLED", True, (255, 0, 0))

    if data["settings"]["popups"]:
        popups_button = font("Regular", 18).render("PopUps: ENABLED", True, (0, 255, 0))
    else:
        popups_button = font("Regular", 18).render("PopUps: DISABLED", True, (255, 0, 0))

    if data["settings"]["music"]:
        music_button = font("Regular", 18).render("Music: ENABLED", True, (0, 255, 0))
    else:
        music_button = font("Regular", 18).render("Music: DISABLED", True, (255, 0, 0))

    if data["settings"]["fps"]:
        fps_button = font("Regular", 18).render("FPS: ENABLED", True, (0, 255, 0))
    else:
        fps_button = font("Regular", 18).render("FPS: DISABLED", True, (255, 0, 0))

    if not owns_sell_plan:
        auto_sell_button = font("Regular", 18).render("Auto Sell: LOCKED", True, (175, 175, 175))
    elif data["settings"]["auto_sell"] and owns_sell_plan:
        auto_sell_button = font("Regular", 18).render("Auto Sell: ENABLED", True, (0, 255, 0))
    elif not data["settings"]["auto_sell"] and owns_sell_plan:
        auto_sell_button = font("Regular", 18).render("Auto Sell: DISABLED", True, (255, 0, 0))

    title_rect = title.get_rect(center=scale_position(257.5, 80))
    sound_effects_rect = sound_effects_button.get_rect(center=scale_position(257.5, 130))
    popups_rect = popups_button.get_rect(center=scale_position(257.5, 170))
    music_rect = music_button.get_rect(center=scale_position(257.5, 210))
    fps_rect = fps_button.get_rect(center=scale_position(257.5, 250))
    auto_sell_rect = auto_sell_button.get_rect(center=scale_position(257.5, 290))

    screen.blit(title, title_rect)
    screen.blit(sound_effects_button, sound_effects_rect)
    screen.blit(popups_button, popups_rect)
    screen.blit(music_button, music_rect)
    screen.blit(fps_button, fps_rect)
    screen.blit(auto_sell_button, auto_sell_rect)

    return {
        "sound_effects": sound_effects_rect,
        "popups": popups_rect,
        "music": music_rect,
        "fps": fps_rect,
        "auto_sell": auto_sell_rect
    }

settings_rects = load_settings()

#[----------------]#
#[----UPGRADES----]#
#[----------------]#

for upgrade in upgrades_list["upgrades"]:
    upgrade_buttons.append(UpgradeButton(scale_position(2335, 50), upgrade, load_scaled, font, scale, data))

upgrade_manager.organize_buttons(upgrade_buttons)

current_store = "upgrades"

upgrades_button = load_scaled("assets/ui/small_frame.png", 160, 64)
upgrades_button_rect = upgrades_button.get_rect(center=(scale_position(2040, 55)))

upgrades_label = font("Regular", sx(20)).render("Upgrades", True, (255, 255, 255))
upgrades_label_rect = upgrades_label.get_rect(center=(scale_position(2040, 57)))

uniques_button = load_scaled("assets/ui/small_frame.png", 160, 64)
uniques_button_rect = uniques_button.get_rect(center=(scale_position(2040, 135)))

uniques_label = font("Regular", sx(22)).render("Uniques", True, (255, 255, 255))
uniques_label_rect = uniques_label.get_rect(center=(scale_position(2040, 137)))

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

clickable_rects = [
    ("options", options_button_rect),
    ("upgrades", upgrades_button_rect),
    ("uniques", uniques_button_rect)
]

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(data)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bug_manager.collect_bug(event.pos, pygame.time.get_ticks(), data, container_manager.rect, bugnet_manager, screen_bugs, popups, scale, font, PopupText)
            upgrade_manager.clicked(upgrade_buttons, mouse_pos, data, scale, popups, font, PopupText)
            phone_manager.clicked(mouse_pos, sellplans_list, data)

            if options_button_rect.collidepoint(mouse_pos) and not options_open:
                options_open = True
            elif options_button_rect.collidepoint(mouse_pos) and options_open:
                options_open = False
            elif stats_rect.collidepoint(mouse_pos):
                if current_frame == None or current_frame == "settings":
                    current_frame = "stats"
                else:
                    current_frame = None
            elif settings_rect.collidepoint(mouse_pos):
                if current_frame == None or current_frame == "stats":
                    current_frame = "settings"
                else:
                    current_frame = None
            elif settings_rects["sound_effects"].collidepoint(mouse_pos):
                data["settings"]["sound_effects"] = not data["settings"]["sound_effects"]
            elif settings_rects["popups"].collidepoint(mouse_pos):
                data["settings"]["popups"] = not data["settings"]["popups"]
            elif settings_rects["music"].collidepoint(mouse_pos):
                data["settings"]["music"] = not data["settings"]["music"]
            elif settings_rects["fps"].collidepoint(mouse_pos):
                data["settings"]["fps"] = not data["settings"]["fps"]
            elif settings_rects["auto_sell"].collidepoint(mouse_pos) and data["owns_auto_sell"]:
                data["settings"]["auto_sell"] = not data["settings"]["auto_sell"]
            elif quit_rect.collidepoint(mouse_pos):
                save_game(data)
                running = False
            elif uniques_button_rect.collidepoint(mouse_pos) and current_store == "upgrades":
                current_store = "uniques"
            elif upgrades_button_rect.collidepoint(mouse_pos) and current_store == "uniques":
                current_store = "upgrades"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSLASH:
                data = default_data.copy()
                save_game(data)
                popups.append(PopupText((screen_width / 2, screen_height /2), "DATA WIPED", font("Regular", 50), (255, 0, 0), 40))

                container_manager.load_container(container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data)
                bugnet_manager.load_bugnet(load_scaled)
                screen_bugs.clear()

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

    if data["settings"]["auto_sell"] and data["owns_auto_sell"]:
        auto_sell_timer += dt * 1000

        auto_sell_interval = data["auto_sell_interval"]

        plan_type = data["sell_plan"]
        sell_cooldown = sellplans_list[plan_type]["cooldown"] * 1000
        total_delay = auto_sell_interval + sell_cooldown

        if auto_sell_timer >= total_delay:
            total = 0

            for bug_name, amount in data["container"]["bugs"].items():
                bug_value = bugs_list[bug_name]["value"]
                total += bug_value * amount

            if total > 0:
                data["currency"] += total
                data["container"]["bugs"] = {}
                data["bugs"] = 0

                container_manager.load_bugs(container_bugs, load_scaled, bugs_list, scale, Bug, data)

                popups.append(PopupText((screen_width / 2, sy(200)), f"+{total} Insectra Auto-Sold", font("Regular", 40), (0, 255, 0), 180))

            auto_sell_timer = 0

    for popup in popups[:]:
        popup.update(scale)
        if popup.dead():
            popups.remove(popup)

    new_container = data["container"]["type"]
    new_bugnet = data["bugnet"]

    if current_container != new_container:
        container_manager.container_name = new_container
        container_manager.load_container(container_bugs, load_scaled, bugs_list, scale, scale_position, Bug, data)
        current_container = new_container
    elif current_bugnet != new_bugnet:
        bugnet_manager.current_bugnet = new_bugnet
        bugnet_manager.bugnet_name = new_bugnet
        bugnet_manager.bugnet_data = bugnets_list[new_bugnet]
        bugnet_manager.load_bugnet(load_scaled)
        current_bugnet = new_bugnet
    
    screen.blit(static_surface, (0, 0))
    screen.blit(container_manager.image, container_manager.rect)

    bug_manager.draw(screen_width, screen_bugs, screen, scale, sx)
    
    screen.blit(options_button, options_button_rect)

    if options_open:
        screen.blit(stats_button, stats_rect)
        screen.blit(settings_button, settings_rect)
        screen.blit(quit_button, quit_rect)

        clickable_rects.extend([
            ("options_frame", options_frame_rect),
            ("stats", stats_rect),
            ("settings", settings_rect),
            ("quit", quit_rect),
            ("upgrades", upgrades_button_rect),
            ("uniques", uniques_button_rect)
        ])
    else:
        current_frame = None
        clickable_rects = [
            ("options", options_button_rect),
            ("upgrades", upgrades_button_rect),
            ("uniques", uniques_button_rect)
        ]

    if current_store == "upgrades":
        upgrades_label = font("Regular", sx(20)).render("Upgrades", True, (25, 255, 25))
        uniques_label = font("Regular", sx(22)).render("Uniques", True, (255, 255, 255))
    elif current_store == "uniques":
        upgrades_label = font("Regular", sx(20)).render("Upgrades", True, (255, 255, 255))
        uniques_label = font("Regular", sx(22)).render("Uniques", True, (25, 255, 25))

    if current_frame != None:
        screen.blit(options_frame, options_frame_rect)

    if current_frame == "stats":
        load_stats()
    if current_frame == "settings":
        load_settings()

    screen.blit(upgrades_button, upgrades_button_rect)
    screen.blit(upgrades_label, upgrades_label_rect)

    screen.blit(uniques_button, uniques_button_rect)
    screen.blit(uniques_label, uniques_label_rect)

    upgrade_manager.draw(upgrade_buttons, screen, data, current_store)
    phone_manager.draw(screen, dt, sy, data, container_manager, container_bugs, load_scaled, bugs_list, scale, Bug)
    bugnet_manager.draw(screen, data, cursor_icon, cursor_icon_rect, scale, load_scaled)
    container_manager.draw(container_bugs, screen, scale, screen_width, sx)

    for popup in popups:
        popup.draw(screen, data)

    fps = clock.get_fps()
    fps_text = font("Regular", 20).render(f"FPS: {int(fps)}", False, (255, 255, 255))
    fps_rect = fps_text.get_rect(midtop=(screen_width // 2, sy(10)))

    if data["settings"]["fps"]:
        screen.blit(fps_text, fps_rect)

    hovering_ui = any(rect.collidepoint(mouse_pos) for _, rect in clickable_rects)
    bugnet_manager.visible = not hovering_ui

    if upgrade_manager.is_hovering(upgrade_buttons, mouse_pos) or phone_manager.is_hovering(mouse_pos):
        bugnet_manager.visible = False

    currency_difference = data["currency"] - display_currency
    step = max(1, abs(currency_difference) // sy(10))

    if currency_difference > 0:
        display_currency += step
    elif currency_difference < 0:
        display_currency -= step

    if display_currency != last_currency:
        currency_text_scale = 1.4
        last_currency = display_currency

    currency_text_scale += (1.0 - currency_text_scale) * 0.2

    currency_text = font("ThinBold", int(sx(50) * currency_text_scale)).render(f"{display_currency:,} Insectra", True, (255, 255, 255))
    shadow_text = font("ThinBold", int(sx(50) * currency_text_scale)).render(f"{display_currency:,} Insectra", True, (0, 0, 0))

    currency_rect = currency_text.get_rect(midtop=(screen_width // 2, sy(40)))
    screen.blit(shadow_text, (currency_rect.x + sx(3), currency_rect.y + sy(3)))
    screen.blit(currency_text, currency_rect)

    pygame.display.flip()