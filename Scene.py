from UI import *
from Lib import *
from Towers import *


class Scene:
    def __init__(self):
        """Override in child classes"""
        pass

    def render(self, screen):
        """Meant to be called once a frame. Override in child classes"""
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

        # Groups for sprites
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Game variables
        self.lives = 20
        self.money = 200
        self.selected_tower = TOWER_BASIC
        self.path = Path(pygame.Color("BLUE"),
                         [(1, -1), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1), (17, 1), (17, 5), (14, 5),
                          (14, 8), (17, 8), (17, 13), (12, 13), (12, 8), (9, 8), (9, 11),(7, 11), (7, 8), (5, 8),
                          (5, 11), (3, 11), (3, 8), (-1, 8)])

    def render(self, screen):
        screen.fill(pygame.Color("BLACK"))
        self.game_screen.fill(FRAME_COLOUR)
        self.game_screen.blit(self.path.image, (0, 0))
        self.towers.draw(self.game_screen)

        # Update mouse selector
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] - 100, mouse_pos[1] - 100)  # To account for the 100x100 border around the outside
        if not self.path.contains(mouse_pos):
            if mouse_pos[0] < self.path.rect.width and mouse_pos[1] < self.path.rect.height:
                if pygame.mouse.get_pressed()[0]:
                    size = 5
                else:
                    size = 2
                pygame.draw.rect(self.game_screen, pygame.Color("WHITE"),
                                 pygame.Rect(mouse_pos[0] - (mouse_pos[0] % GRID_SIZE),
                                 mouse_pos[1] - (mouse_pos[1] % GRID_SIZE),
                                 GRID_SIZE, GRID_SIZE), size)
        screen.blit(self.game_screen, self.rect)
