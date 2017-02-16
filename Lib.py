import pygame, math

# Colours
BACKGROUND_COLOUR = pygame.Color("GRAY")
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # AQUA
TEXT_COLOUR = pygame.Color("WHITE")
TOOLBAR_COLOUR = pygame.Color(60, 60, 60, 0)  # Dark Grey

# Directions
NORTH = 0
UP = 0
EAST = 1
RIGHT = 1
SOUTH = 2
DOWN = 2
WEST = 3
LEFT = 3

# Game states
STATE_MAIN_MENU = 1
STATE_PRE_WAVE = 2
STATE_WAVE = 3
STATE_PAUSED = 4
STATE_GAME_OVER = 5

# Custom events
ENEMY_REACHED_END = pygame.USEREVENT+1
WAVE_STARTED = pygame.USEREVENT+2
ENEMY_KILLED = pygame.USEREVENT+3
TOWER_BOUGHT = pygame.USEREVENT+4
EVENT_STATE_CHANGED = pygame.USEREVENT+5


def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])


def gridCoordToPos(grid_coord, grid_size):
    return tuple([grid_coord[0]*grid_size + grid_size//2, grid_coord[1]*grid_size + grid_size//2])


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def getDirection(pos1, pos2):
    if abs(pos1[0]-pos2[0]) > abs(pos1[1]-pos2[1]):
        if pos1[0] > pos2[0]:
            return WEST
        else:
            return EAST
    else:
        if pos1[1] > pos2[1]:
            return NORTH
        else:
            return SOUTH


class Path(pygame.sprite.Sprite):
    def __init__(self, colour, waypoints=[], grid_size=50):
        pygame.sprite.Sprite.__init__(self)

        # Find furthest points of the path so the surface is the correct size
        highest_x = 0
        highest_y = 0
        for point in waypoints:
            if point[0] > highest_x:
                highest_x = point[0]
            if point[1] > highest_y:
                highest_y = point[1]
        print((highest_x, highest_y))

        self.image = pygame.Surface(((highest_x+1)*50, (highest_y+1)*50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.colour = colour
        self.waypoints = waypoints
        self.grid_size = grid_size
        self.rectangles = []
        self.generateRectangles()

    def addToPath(self, coords):
        self.waypoints.append(coords)
        self.generateRectangles()

    def generateRectangles(self):
        self.rectangles = []
        for i in range(len(self.waypoints)-1):
            first_pos = self.waypoints[i]
            second_pos = self.waypoints[i + 1]
            if first_pos[0] == second_pos[0]:
                if first_pos[1] <= second_pos[1]:
                    top_left = first_pos
                    bottom_right = second_pos
                else:
                    top_left = second_pos
                    bottom_right = first_pos
            else:
                if first_pos[0] <= second_pos[0]:
                    top_left = first_pos
                    bottom_right = second_pos
                else:
                    top_left = second_pos
                    bottom_right = first_pos

            rect = pygame.Rect(top_left[0]*self.grid_size,
                               top_left[1]*self.grid_size,
                               (bottom_right[0]+1-top_left[0])*self.grid_size,
                               (bottom_right[1] + 1 - top_left[1]) * self.grid_size)
            pygame.draw.rect(self.image, self.colour, rect)
            self.rectangles.append(rect)

    def contains(self, point):
        for rect in self.rectangles:
            if rect.collidepoint(point):
                return True
        return False

