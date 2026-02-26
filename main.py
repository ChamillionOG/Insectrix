#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import pygame

from upgradeButtons import UpgradeManager, UpgradeButton
from containerManager import ContainerManager
from bugnetManager import BugnetManager
from popupText import PopupTextManager
from phoneManager import PhoneManager
from savesManager import load_data
from bugManager import BugManager

#[------------]#
#[----DATA----]#
#[------------]#

data = load_data()

print(f"Save Data: {data}")

def main():

    #[-------------]#
    #[----SETUP----]#
    #[-------------]#

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Insectrix")
    current_enviroment = data["enviroment"]
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    spawn_timer = 0
    spawn_delay = 1000

    enviroment_background = pygame.image.load(f"assets/images/enviroments/{current_enviroment}.png")
    enviroment_background = pygame.transform.scale(enviroment_background, (screen_width, screen_height))

    in_container_bugs = []
    on_screen_bugs = []

    ##[ -- Manager Handlers -- ]##

    popup_manager = PopupTextManager()                                                              # --- Popup Manager
    container_manager = ContainerManager(data["container"], screen_height, in_container_bugs, data) # --- Container Manager
    phone_manager = PhoneManager(screen_width, screen_height, container_manager, data, "off")             # --- Phone Manager
    bug_manager = BugManager(data["enviroment"], on_screen_bugs, in_container_bugs, popup_manager)  # --- Bug Manager
    bugnet_manager = BugnetManager(data["bugnet"], (0, 0))                                          # --- Bugnet Manager
    upgrade_manager = UpgradeManager(25, -55, popup_manager, data)                                  # --- Upgrade Button Manager

    container_manager.loadBugs(data)

    ##[ -- Button Information -- ]##

    font = pygame.font.Font("assets/rainyhearts.ttf", 35)
    frame_image = pygame.image.load("assets/ui/buttonFrame.png")
    upgrade_icons_path = "assets/images/upgradeIcons/"

    buttons_list = [
        UpgradeButton(0, 0, 300, 200, frame_image, pygame.image.load(f"{upgrade_icons_path}sturdy_bugnet_icon.png"),  "Sturdy Bugnet", 1, font, effect=lambda v: v.__setitem__("bugnet", "sturdy"))
    ]

    for button in buttons_list:
        if not data["purchases"].get(button.name, False): # --- If player does not own upgrade, display it
            upgrade_manager.add_button(button, screen_width)

    running = True

    #[----------------]#
    #[----GAMELOOP----]#
    #[----------------]#

    while running:

        ##[ -- Input Handling -- ]##

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bug_manager.collect_bug(event.pos, container_manager.container_image_rect, data, pygame.mouse, bugnet_manager) # --- Bug Clicked
                upgrade_manager.handle_click(event.pos)                                                                        # --- Button Clicked
                phone_manager.handle_click(event.pos)                                                                          # --- Phone Clicked
                bugnet_manager.swing(data)                                                                                     # --- Bugnet Swung

        screen.blit(enviroment_background, (0, 0))
        dt = clock.tick(60) / 1000
        spawn_timer += dt * 1000

        ##[ -- Bug Spawning -- ]##

        if spawn_timer >= spawn_delay and len(on_screen_bugs) < data["max_bugs"]:
            bug_manager.spawn_bug(screen_width, screen_height)
            spawn_timer = 0

        ##[ -- Cursor Icon Handler -- ]##

        mouse_pos = pygame.mouse.get_pos()

        if upgrade_manager.is_hovering(mouse_pos) or phone_manager.is_hovering(mouse_pos):
            bugnet_manager.visible = False
        else:
            bugnet_manager.visible = True

        ##[ -- Visual Updates -- ]##

        upgrade_manager.draw(screen)                      # --- Upgrade Draw
        phone_manager.update(screen, dt)                  # --- Phone Update
        bugnet_manager.update(screen, pygame.mouse, data) # --- Bugnet Update
        bug_manager.update(screen_width, screen)          # --- Bug Update
        container_manager.update(screen)                  # --- Container Update
        popup_manager.update(dt)                          # --- Popup Update
        popup_manager.draw(screen)                        # --- Popup Draw
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()