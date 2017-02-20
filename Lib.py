import pygame, math

# Colours
FRAME_COLOUR = pygame.Color("BLACK")
BACKGROUND_COLOUR = pygame.Color("GRAY")
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # AQUA
TEXT_COLOUR = pygame.Color("WHITE")
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60, 0)  # Dark Grey
BUTTON_DISABLED_COLOUR = pygame.Color("RED")
PATH_COLOUR = pygame.Color("BLUE")
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")

# Global variables
GRID_SIZE = 50

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Game states
STATE_MAIN_MENU = 1
STATE_PRE_WAVE = 2
STATE_WAVE = 3
STATE_PAUSED = 4
STATE_GAME_OVER = 5

# Custom events
ENEMY_REACHED_END = pygame.USEREVENT+1
ENEMY_KILLED = pygame.USEREVENT+2
TOWER_BOUGHT = pygame.USEREVENT+3
EVENT_STATE_CHANGED = pygame.USEREVENT+4


def negateCoords(coords):
    return tuple([-coords[0], -coords[1]])


def adjustCoordsByOffset(coords, offset):
    return tuple([coords[0]-offset[0], coords[1]-offset[1]])


def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])


def gridCoordToPos(grid_coord, grid_size):
    return tuple([grid_coord[0]*grid_size + grid_size//2, grid_coord[1]*grid_size + grid_size//2])


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def getDirection(pos1, pos2):
    if abs(pos1[0]-pos2[0]) > abs(pos1[1]-pos2[1]):
        if pos1[0] > pos2[0]:
            return LEFT
        else:
            return RIGHT
    else:
        if pos1[1] > pos2[1]:
            return UP
        else:
            return DOWN


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

        self.image = pygame.Surface(((highest_x+3)*GRID_SIZE, (highest_y+3)*GRID_SIZE))
        self.image.fill(BACKGROUND_COLOUR)
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

