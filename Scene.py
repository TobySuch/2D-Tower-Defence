from UI import *
from Towers import *
from Wave import *
from Enemies import *


class Scene:
    """Abstract class"""
    def __init__(self, screen_size, screen):
        """Override in child classes"""
        # Creates a sub surface as the game screen.
        # This means anything blitted to the game screen is automatically put on the screen (more efficient)
        # Also handles relative coords with get_abs_offset()
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)

    def update(self, **kwargs):
        """Updates the scene. Meant to be called once a frame. Override in child classes"""
        pass

    def render(self, **kwargs):
        """Renders the scene. Meant to be called once a frame. Override in child classes"""
        pass


class GameOver(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect((0, 0), screen_size)
        self.screen = screen.subsurface(self.rect)
        self.title = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//3), (600, 100)), "GAME OVER", TEXT_COLOUR, 100)
        self.survival_message = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//2), (600, 100)), "You survived until wave 999", TEXT_COLOUR, 50)
        self.main_menu_button = Button(pygame.Rect((screen_size[0]//2-225, 2*screen_size[1]//3-50), (450, 100)), "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 100)

    def render(self, **kwargs):
        self.screen.blit(self.title.image, self.title.rect)
        self.screen.blit(self.survival_message.image, self.survival_message.rect)
        self.screen.blit(self.main_menu_button.image, self.main_menu_button.rect)


class MainMenu(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.menu_screen = screen.subsurface(self.rect)

        self.title = TextDisplay(pygame.Rect(0, 100, screen_size[0], 100), "Tower Defence Game", TEXT_COLOUR, 100)

        self.instructions = []
        self.instructions.append(TextDisplay(pygame.Rect(0, 300, screen_size[0], 65), "Left click a free space to place a tower", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 365, screen_size[0], 65), "Click a tower in the shop or press a number to change the tower you place", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 430, screen_size[0], 65), "Right click a tower to sell it", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 495, screen_size[0], 65), "Press 'Next wave' or press the space bar to start the wave", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 560, screen_size[0], 65), "Try to survive as long as you can", TEXT_COLOUR, 50))

        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 150, 630, 150, 80),
                                  "Play", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 50, 630, 150, 80),
                                  "Quit", BUTTON_COLOUR, TEXT_COLOUR, 50)

        self.music_credit = TextDisplay(pygame.Rect(100, 900, 700, 50), "Music: 'Quando a revolução vier' by OVO (Released under CC)", TEXT_COLOUR, 30)

    def render(self, **kwargs):
        self.menu_screen.blit(self.title.image, self.title.rect)
        for instruction in self.instructions:
            self.menu_screen.blit(instruction.image, instruction.rect)
        self.menu_screen.blit(self.play_button.image, self.play_button.rect)
        self.menu_screen.blit(self.quit_button.image, self.quit_button.rect)
        self.menu_screen.blit(self.music_credit.image, self.music_credit.rect)


class Pause(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.pause_overlay = screen.subsurface(self.rect)
        self.pause_message = TextDisplay(pygame.Rect(360, 200, 180, 60), "PAUSED", TEXT_COLOUR, 50)
        self.resume_button = Button(pygame.Rect(200, 340, 225, 75),
                                    "Resume", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect(475, 340, 225, 75),
                                  "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 50)

    def render(self, **kwargs):
        kwargs["SCENE_GAME"].render(screen=kwargs["screen"], current_state=kwargs["current_state"])
        self.pause_overlay.blit(self.pause_message.image, self.pause_message.rect)
        self.pause_overlay.blit(self.resume_button.image, self.resume_button.rect)
        self.pause_overlay.blit(self.quit_button.image, self.quit_button.rect)


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

        # Game variables
        self.lives = 20
        self.money = 200
        self.selected_tower = 0
        self.path = Path(PATH_COLOUR,
                         [(1, -1), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1), (17, 1), (17, 5), (14, 5),
                          (14, 8), (17, 8), (17, 13), (12, 13), (12, 8), (9, 8), (9, 11), (7, 11), (7, 8), (5, 8),
                          (5, 11), (3, 11), (3, 8), (-1, 8)])
        self.wave_handler = WaveHandler(self.path.waypoints[0])
        self.enemies_alive = 0

        # Tower models (available towers to build)
        self.tower_models = []
        tower_model = TowerModel("Basic Tower", 1, 20, 2, 100, pygame.Color("GREEN"), 'assets/tower1.png', "Low damage, low range, high firerate")
        self.tower_models.append(tower_model)
        tower_model = TowerModel("Sniper Tower", 3, 100, 5, 300, pygame.Color("WHITE"), 'assets/tower2.png', "High damage, high range, low firerate")
        self.tower_models.append(tower_model)

        # Top bar elements
        self.next_wave_button = Button(pygame.Rect(100, 25, 160, 50), "Next Wave", BUTTON_COLOUR, TEXT_COLOUR, 40)
        self.pause_button = Button(pygame.Rect(270, 25, 95, 50), "Pause", BUTTON_DISABLED_COLOUR, TEXT_COLOUR, 40)
        self.wave_display = TextDisplay(pygame.Rect(375, 25, 210, 50), "Current Wave: " + str(self.wave_handler.current_wave_number), TEXT_COLOUR, 30)
        self.enemy_count_display = TextDisplay(pygame.Rect(595, 25, 280, 50), "Enemies Remaining: " + str(self.enemies_alive), TEXT_COLOUR, 30)
        self.lives_display = TextDisplay(pygame.Rect(885, 25, 120, 50), "Lives: " + str(self.lives), TEXT_COLOUR, 30)
        self.money_display = TextDisplay(pygame.Rect(1015, 25, 160, 50), "Money: " + str(self.money), TEXT_COLOUR, 30)

        # Shop elements
        self.shop = Shop(screen, pygame.Rect(adjustCoordsByOffset(self.path.rect.topright, (-self.offset[0], -self.offset[1])), (400, self.path.rect.height)), self.tower_models)

    def update(self, **kwargs):
        self.wave_handler.update(self.enemies)
        self.enemies.update(self.path.waypoints, GRID_SIZE)
        self.towers.update(self.enemies, self.effects, self.game_screen)
        self.effects.update()
        self.money_display.text = "Money: " + str(self.money)

    def render(self, **kwargs):
        screen = kwargs['screen']
        screen.fill(pygame.Color("BLACK"))

        # Render top bar
        screen.blit(self.next_wave_button.image, self.next_wave_button.rect)
        screen.blit(self.pause_button.image, self.pause_button.rect)
        screen.blit(self.wave_display.image, self.wave_display.rect)
        screen.blit(self.enemy_count_display.image, self.enemy_count_display.rect)
        screen.blit(self.lives_display.image, self.lives_display.rect)
        screen.blit(self.money_display.image, self.money_display.rect)

        # Render Game
        self.game_screen.fill(FRAME_COLOUR)
        self.game_screen.blit(self.path.image, (0, 0))
        self.enemies.draw(self.game_screen)
        self.towers.draw(self.game_screen)
        self.effects.draw(self.game_screen)

        # Render shop
        self.shop.render(self.selected_tower)

        # Update mouse selector
        if kwargs["current_state"] != STATE_PAUSED:  # Won't display mouse selector if game is paused
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])  # Accounts for the border
            if not self.path.contains(mouse_pos):
                if 0 < mouse_pos[0] < self.path.rect.width and 0 < mouse_pos[1] < self.path.rect.height:
                    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # Mouse selector is bigger if the mouse button is down
                        size = 5
                    else:
                        size = 2
                    pygame.draw.rect(self.game_screen, MOUSE_SELECTOR_COLOUR,
                                     pygame.Rect(mouse_pos[0] - (mouse_pos[0] % GRID_SIZE),
                                                 mouse_pos[1] - (mouse_pos[1] % GRID_SIZE),
                                                 GRID_SIZE, GRID_SIZE), size)

