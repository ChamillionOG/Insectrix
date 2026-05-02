class EnvironmentManager:
    def __init__(self, current_environment, environments_list):
        self.current_environment = current_environment
        self.environments_list = environments_list

        self.environment_name = self.current_environment

    def load_environment(self, load_scaled, data):
        image = load_scaled(f"assets/images/environments/{self.environment_name}.png", 2560, 1440)
        data["environment_multiplier"] = self.environments_list[self.current_environment]["multiplier"]

        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)