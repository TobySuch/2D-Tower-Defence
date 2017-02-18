import pygame
from Lib import *


def createEnemy(pos):
    enemy = Enemy(pos, 2, 3)
    return enemy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, current_waypoint=1):
        pygame.sprite.Sprite.__init__(self)
        self.base_sprite = pygame.image.load('assets/enemy1.png')
        self.image = self.base_sprite
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.health = health
        self.current_waypoint = current_waypoint
        self.direction = None
        self.value = 5
        self.distance_travelled = 0
        self.is_dead = False

    def update(self, waypoints, grid_size):
        waypoint = waypoints[self.current_waypoint]

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

            # Set orientation
            if self.direction == LEFT:
                self.image = pygame.transform.rotate(self.base_sprite, 90)
            elif self.direction == DOWN:
                self.image = pygame.transform.rotate(self.base_sprite, 180)
            elif self.direction == RIGHT:
                self.image = pygame.transform.rotate(self.base_sprite, 270)
            else:
                self.image = pygame.transform.rotate(self.base_sprite, 0)

        # Move towards next waypoint
        self.distance_travelled += self.speed
        if self.direction == UP:
            self.rect.move_ip((0, -self.speed))
            # Moves sprite into the middle of the path, not ideal but whatever
            self.rect.centerx = waypoint[0]*grid_size + grid_size//2
        elif self.direction == LEFT:
            self.rect.move_ip((-self.speed, 0))
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2
        elif self.direction == DOWN:
            self.rect.move_ip((0, self.speed))
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2
        else:
            self.rect.move_ip((self.speed, 0))
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2

