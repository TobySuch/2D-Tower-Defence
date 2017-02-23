import pygame
from Lib import *


def createEnemy(pos):
    enemy = Enemy(pos, 2, 3)
    return enemy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, current_waypoint=1):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load('assets/enemy1.png')
        self.image = None
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.center = pos
        self.speed = speed
        self.health = health
        self.current_waypoint = current_waypoint
        self.direction = None
        self.value = 5
        self.distance_travelled = 0
        self.is_dead = False
        self.current_image = (0, 0)

    def update(self, waypoints, grid_size):
        waypoint = waypoints[self.current_waypoint]

        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), pygame.Rect(self.current_image[0]*self.rect.width, self.current_image[1]*self.rect.height, self.rect.width, self.rect.height))

        if self.current_image[0]+1 >= self.spritesheet.get_width()//self.rect.width:
            if self.current_image[1]+1 >= self.spritesheet.get_height()//self.rect.height:
                self.current_image = (0, 0)
            else:
                self.current_image = (0, self.current_image[1]+1)
        else:
            self.current_image = (self.current_image[0] + 1, self.current_image[1])

        if self.direction is None or self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
            if self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
                # Reached waypoint
                if self.current_waypoint < len(waypoints)-1:
                    self.current_waypoint += 1
                else:
                    # Enemy has reached end of path
                    pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))
            waypoint = waypoints[self.current_waypoint]
            self.direction = getDirection(posToGridCoords(self.rect.center, grid_size), waypoint)

        # Move towards next waypoint
        self.distance_travelled += self.speed
        if self.direction == UP:
            self.rect.move_ip((0, -self.speed))
            # Moves sprite into the middle of the path, not ideal but whatever
            self.rect.centerx = waypoint[0]*grid_size + grid_size//2
        elif self.direction == LEFT:
            self.rect.move_ip((-self.speed, 0))
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2
            self.image = pygame.transform.rotate(self.image, 90)  # Set orientation
        elif self.direction == DOWN:
            self.rect.move_ip((0, self.speed))
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.rect.move_ip((self.speed, 0))
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2
            self.image = pygame.transform.rotate(self.image, 270)

