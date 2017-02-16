from UI import *


class Scene:
    def __init__(self):
        """Override in child classes"""
        pass

    def render(self, screen):
        """Override in child classes"""
        pass


class MainMenu(Scene):
    def __init__(self, screen_size, button_colour, text_colour):
        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 600, (screen_size[1]/2) - 100, 400, 200),
                                  "Play", button_colour, text_colour)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 200, (screen_size[1]/2) - 100, 400, 200),
                                  "Quit", button_colour, text_colour)

    def render(self, screen):
        screen.blit(self.play_button.image, self.play_button.rect)
        screen.blit(self.quit_button.image, self.quit_button.rect)


class Game(Scene):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.rect = pygame.Rect(100, 100, screen_size[0] - 200, screen_size[1] - 200)
        self.game_screen = pygame.Surface((self.rect.width, self.rect.height))

    def render(self, screen, player, enemies):
        player.update()
        enemies.update()
        self.game_screen.fill(pygame.Color("BLACK"))
        self.game_screen.blit(player.image, player.rect.topleft)
        screen.blit(self.game_screen, self.rect)
