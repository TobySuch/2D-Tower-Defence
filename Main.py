from Scene import *
from Lib import *

# Pygame init
pygame.init()
display_info = pygame.display.Info()

# Constants
SCREEN_SIZE = (display_info.current_w, display_info.current_h)

# Global variables
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Setup scenes
SCENE_MAIN_MENU = MainMenu(SCREEN_SIZE, screen)
SCENE_GAME = None  # This scene is not initialised as it will be reset when they click play

# State holders
done = False
current_state = STATE_MAIN_MENU
current_scene = SCENE_MAIN_MENU

# Main loop
while not done:
    # Wipe currently displayed scene
    screen.fill(BACKGROUND_COLOUR)

    # Process and render current scene
    current_scene.render(screen=screen)

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
                    SCENE_GAME = Game(SCREEN_SIZE, screen)  # Creates a new game instance
                    current_scene = SCENE_GAME
                    current_state = STATE_PRE_WAVE
            elif event.next_state == STATE_WAVE:
                current_state = STATE_WAVE
                SCENE_GAME.wave_handler.start_wave()
                SCENE_GAME.next_wave_button.background_colour = pygame.Color("RED")
                SCENE_GAME.enemies_alive = SCENE_GAME.wave_handler.current_wave.enemies
                # TODO: Enable pause button

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
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Check if toolbar buttons were pressed
                    if SCENE_GAME.next_wave_button.contains(event.pos):
                        if current_state == STATE_PRE_WAVE:  # Button can only be pressed during pre-wave
                            pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))
                    else:
                        # Placed a tower
                        mouse_pos = (event.pos[0]-SCENE_GAME.offset[0], event.pos[1]-SCENE_GAME.offset[1])  # To account for the 100x100 border around the outside
                        if not SCENE_GAME.path.contains(mouse_pos):
                            if 0 < mouse_pos[0] < SCENE_GAME.path.rect.width and 0 < mouse_pos[1] < SCENE_GAME.path.rect.height:  # Make sure tower is on game screen
                                tower = createTower(gridCoordToPos(posToGridCoords(mouse_pos, GRID_SIZE), GRID_SIZE), SCENE_GAME.path, SCENE_GAME.towers)
                                if tower is not None and tower.value <= SCENE_GAME.money:
                                    SCENE_GAME.towers.add(tower)
                                    SCENE_GAME.money -= tower.value
            elif event.type == ENEMY_KILLED:
                SCENE_GAME.enemies_alive -= 1
                SCENE_GAME.money += event.enemy.value
                event.enemy.kill()
            elif event.type == ENEMY_REACHED_END:
                SCENE_GAME.lives -= 1
                if SCENE_GAME.lives <= 0:
                    # Game Over
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_GAME_OVER))
                else:
                    # Move the enemy back to the start
                    event.enemy.current_waypoint = 1
                    event.enemy.rect.center = gridCoordToPos(SCENE_GAME.path.waypoints[0], GRID_SIZE)
                    event.enemy.distance_travelled = 0

    # Display frame
    pygame.display.flip()

    # Keep frame rate constant
    clock.tick(60)