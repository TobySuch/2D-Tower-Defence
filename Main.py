from Scene import *

# Pygame init
pygame.init()
display_info = pygame.display.Info()

# Constants
SCREEN_SIZE = (display_info.current_w, display_info.current_h)
BACKGROUND_COLOUR = pygame.Color("GRAY")
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # AQUA
TEXT_COLOUR = pygame.Color("WHITE")

# Custom Events
EVENT_STATE_CHANGED = pygame.USEREVENT + 1

# Game states
STATE_MAIN_MENU = 1
STATE_PRE_WAVE = 2
STATE_WAVE = 3
STATE_PAUSED = 4
STATE_GAME_OVER = 5

# Setup scenes
SCENE_MAIN_MENU = MainMenu(SCREEN_SIZE, BUTTON_COLOUR, TEXT_COLOUR)
SCENE_GAME = None  # This scene is not initialised as it will be reset when they click play

# Global variables
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
done = False
current_state = STATE_MAIN_MENU
current_scene = SCENE_MAIN_MENU
sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Main loop
while not done:
    # Wipe currently displayed scene
    screen.fill(BACKGROUND_COLOUR)

    # Process and render current scene
    if current_state == STATE_MAIN_MENU:
        current_scene.render(screen)
    if current_state == STATE_PRE_WAVE or current_state == STATE_WAVE:
        current_scene.render(screen)

    # Handle events
    for event in pygame.event.get():
        # Global Events (Happen across all scenes)
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.type == EVENT_STATE_CHANGED:
            if event.next_state == STATE_PRE_WAVE:
                if current_state == STATE_WAVE:
                    pass
                elif current_state == STATE_PAUSED:
                    pass
                else:
                    SCENE_GAME = Game(SCREEN_SIZE)  # Creates a new game instance
                    current_scene = SCENE_GAME
                    current_state = STATE_PRE_WAVE

        # Main menu events
        if current_scene == SCENE_MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if SCENE_MAIN_MENU.play_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))
                    elif SCENE_MAIN_MENU.quit_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        # In game events
        elif current_scene == SCENE_GAME:
            pass

    # Display frame
    pygame.display.flip()

    # Keep frame rate constant
    clock.tick(60)