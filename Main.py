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
SCENE_PAUSE = Pause(SCREEN_SIZE, screen)

# State holders
done = False
current_state = STATE_MAIN_MENU
current_scene = SCENE_MAIN_MENU

# Main loop
while not done:
    # Wipe currently displayed scene
    screen.fill(BACKGROUND_COLOUR)

    # Update current scene
    current_scene.update()

    # Render current scene
    current_scene.render(screen=screen, current_state=current_state, SCENE_GAME=SCENE_GAME)

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
                    # Wave just ended
                    current_state = STATE_PRE_WAVE
                    SCENE_GAME.next_wave_button.background_colour = BUTTON_COLOUR
                    SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                elif current_state == STATE_PAUSED:
                    # Game unpaused
                    # TODO: Implement Paused
                    pass
                else:
                    # New game
                    SCENE_GAME = Game(SCREEN_SIZE, screen)  # Creates a new game instance
                    current_scene = SCENE_GAME
                    current_state = STATE_PRE_WAVE
            elif event.next_state == STATE_WAVE:
                current_state = STATE_WAVE
                SCENE_GAME.wave_handler.start_wave()
                SCENE_GAME.next_wave_button.background_colour = BUTTON_DISABLED_COLOUR
                SCENE_GAME.enemies_alive = SCENE_GAME.wave_handler.current_wave.enemies
                SCENE_GAME.enemy_count_display.text = "Enemies Remaining: " + str(SCENE_GAME.enemies_alive)
                SCENE_GAME.pause_button.background_colour = BUTTON_COLOUR
                SCENE_GAME.wave_display.text = "Current Wave: " + str(SCENE_GAME.wave_handler.current_wave_number)
            elif event.next_state == STATE_PAUSED:
                current_state = STATE_PAUSED
                SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                current_scene = SCENE_PAUSE



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
                    elif SCENE_GAME.pause_button.contains(event.pos):
                        if current_state == STATE_WAVE:  # Button can only be pressed during the wave
                            pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PAUSED))
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
                SCENE_GAME.enemy_count_display.text = "Enemies Remaining: " + str(SCENE_GAME.enemies_alive)
                SCENE_GAME.money += event.enemy.value
                event.enemy.kill()
                if SCENE_GAME.enemies_alive <= 0:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))
            elif event.type == ENEMY_REACHED_END:
                SCENE_GAME.lives -= 1
                SCENE_GAME.lives_display.text = "Lives: " + str(SCENE_GAME.lives)
                if SCENE_GAME.lives <= 0:
                    # Game Over
                    # TODO: Implement Game Over
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