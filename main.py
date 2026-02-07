import pygame

from upgradeButtons import UpgradeManager, UpgradeButton
from containerManager import ContainerManager
from bugnetManager import BugnetManager
from popupText import PopupTextManager
from savesManager import load_data
from bugManager import BugManager

data = load_data()

print(f"Save Data: {data}")

def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Insectrix")
    current_enviroment = data["enviroment"]
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    font = pygame.font.Font("assets/rainyhearts.ttf", 35)
    frame_image = pygame.image.load("assets/ui/buttonFrame.png")
    icon_image = pygame.image.load("assets/images/gameIcon.png")

    enviroment_background = pygame.image.load(f"assets/images/enviroments/{current_enviroment}.png")
    enviroment_background = pygame.transform.scale(enviroment_background, (screen_width, screen_height))

    in_container_bugs = []
    on_screen_bugs = []

    popup_manager = PopupTextManager()
    container_manager = ContainerManager(data["container"], screen_height, in_container_bugs, data)
    bug_manager = BugManager(data["enviroment"], on_screen_bugs, in_container_bugs, popup_manager)
    bugnet_manager = BugnetManager(data["bugnet"], (0, 0))
    upgrade_manager = UpgradeManager(-50, -75, popup_manager, data)

    container_manager.loadBugs(data)

    spawn_timer = 0
    spawn_delay = 1000

    buttons_list = [
        UpgradeButton(50, 0, 500, 300, frame_image, icon_image, "Test", 1, font),
        UpgradeButton(50, 0, 500, 300, frame_image, icon_image, "Test2", 2, font),
        UpgradeButton(50, 0, 500, 300, frame_image, icon_image, "Test3", 3, font),
    ]

    for button in buttons_list:
        upgrade_manager.add_button(button, screen_width)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bug_manager.collect_bug(event.pos, container_manager.container_image_rect, data, pygame.mouse)
                upgrade_manager.handle_click(event.pos)
                bugnet_manager.swing()
                
        screen.blit(enviroment_background, (0, 0))
        spawn_timer += clock.get_time()
        dt = clock.tick(60) / 1000

        if spawn_timer >= spawn_delay and len(on_screen_bugs) < data["max_bugs"]:
            bug_manager.spawn_bug(screen_width, screen_height)
            spawn_timer = 0

        bugnet_manager.update(screen, pygame.mouse, data)
        bug_manager.update(screen_width, screen)
        container_manager.update(screen)
        popup_manager.update(dt)
        popup_manager.draw(screen)
        upgrade_manager.draw(screen)
        
        pygame.display.flip()
        clock.tick(180)

    pygame.quit()

if __name__ == "__main__":
    main()