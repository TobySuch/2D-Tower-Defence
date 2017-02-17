from UI import *
from Lib import *
from Towers import *


class Scene:
    def __init__(self, screen_size, screen):
        """Override in child classes"""
        # Creates a sub surface as the game screen.
        # This means anything blitted to the game screen is automatically put on the screen
        # Also handles relative coords with get_abs_offset()
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)

    def render(self, **kwargs):
        """Updates and renders the scene. Meant to be called once a frame. Override in child classes"""
        pass


class MainMenu(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.menu_screen = screen.subsurface(self.rect)

        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 600, (screen_size[1]/2) - 100, 400, 200),
                                  "Play", BUTTON_COLOUR, TEXT_COLOUR, 100)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 200, (screen_size[1]/2) - 100, 400, 200),
                                  "Quit", BUTTON_COLOUR, TEXT_COLOUR, 100)

    def render(self, **kwargs):
        self.menu_screen.blit(self.play_button.image, self.play_button.rect)
        self.menu_screen.blit(self.quit_button.image, self.quit_button.rect)


class Game(Scene):
    def __init__(self, screen_size, screen):
        self.screen_size = screen_size
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)
        self.offset = self.game_screen.get_abs_offset()

        # Groups for sprites
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        #Buttons
        self.next_wave_button = Button(pygame.Rect(100, 25, 200, 50), "Next Wave", BUTTON_COLOUR, TEXT_COLOUR, 45)

        # Game variables
        self.lives = 20
        self.money = 200
        self.selected_tower = TOWER_BASIC
        self.path = Path(pygame.Color("BLUE"),
                         [(1, -1), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1), (17, 1), (17, 5), (14, 5),
                          (14, 8), (17, 8), (17, 13), (12, 13), (12, 8), (9, 8), (9, 11),(7, 11), (7, 8), (5, 8),
                          (5, 11), (3, 11), (3, 8), (-1, 8)])

    def render(self, **kwargs):
        screen = kwargs['screen']
        screen.fill(pygame.Color("BLACK"))

        # Render Buttons
        screen.blit(self.next_wave_button.image, self.next_wave_button.rect)

        # Render Game
        self.game_screen.fill(FRAME_COLOUR)
        self.game_screen.blit(self.path.image, (0, 0))
        self.enemies.update()
        self.towers.update(self.enemies, self.effects, self.game_screen)
        self.effects.update()
        self.towers.draw(self.game_screen)

        # Update mouse selector
        mouse_pos = pygame.mouse.get_pos()

        mouse_pos = (mouse_pos[0]-self.offset[0], mouse_pos[1]-self.offset[1])  # Accounts for the border
        if not self.path.contains(mouse_pos):
            if 0 < mouse_pos[0] < self.path.rect.width and 0 < mouse_pos[1] < self.path.rect.height:
                if pygame.mouse.get_pressed()[0]:
                    size = 5
                else:
                    size = 2
                pygame.draw.rect(self.game_screen, pygame.Color("WHITE"),
                                 pygame.Rect(mouse_pos[0] - (mouse_pos[0] % GRID_SIZE),
                                 mouse_pos[1] - (mouse_pos[1] % GRID_SIZE),
                                 GRID_SIZE, GRID_SIZE), size)
