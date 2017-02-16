from Lib import *
from Effects import *

TOWER_BASIC = 1
TOWER_SNIPER = 2

def createTower(pos, path, towers):
    if not path.contains(pos):  # Check point is not on path
        for tower in towers.sprites():  # Check tower does not already exist there
            if tower.rect.collidepoint(pos):
                return None
        tower = Tower(1, 20, 2, 100, pos, pygame.Color("GREEN"))
        return tower
    return None


class Tower(pygame.sprite.Sprite):
    def __init__(self, damage, fire_rate, range, value, pos, fire_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/tower1.png')
        self.rect = self.image.get_rect()
        self.damage = damage
        self.fire_rate = fire_rate
        self.range = range
        self.rect.center = pos
        self.last_fired = 0;
        self.value = value
        self.fire_colour = fire_colour

    def update(self, enemies, effects, screen, grid_size):
        if self.last_fired <= self.fire_rate:
            self.last_fired += 1
        else:
            # Look for target to fire at
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.range * grid_size + 1:
                        if target is None or sprite.distance_travelled > target.distance_travelled:
                            target = sprite
            if target is not None:
                # FIRE ZE MISSILEZZ!
                target.health -= self.damage
                effects.add(Effect(self.fire_colour, target.rect.center, self.rect.center, 2, screen.get_size()))
                if target.health <= 0:
                    target.is_dead = True
                    pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=target))
                self.last_fired = 0

