from Lib import *
from Effects import *


def createTower(pos, tower_choice, tower_models, path, towers):
    if not path.contains(pos):  # Check point is not on path
        for tower in towers.sprites():  # Check tower does not already exist there
            if tower.rect.collidepoint(pos):
                return None
        tower = Tower(pos, tower_models[tower_choice])
        return tower
    return None


class TowerModel:
    def __init__(self, name, damage, fire_rate, range, value, fire_colour, sprite_location, description):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.range = range
        self.value = value
        self.fire_colour = fire_colour
        self.sprite_location = sprite_location
        self.description = description


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        pygame.sprite.Sprite.__init__(self)
        self.model = model
        self.image = pygame.image.load(model.sprite_location)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_fired = 0;

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            # Look for target to fire at
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        if target is None or sprite.distance_travelled > target.distance_travelled:
                            target = sprite
            if target is not None:
                # FIRE ZE MISSILEZZ!
                target.health -= self.model.damage
                effects.add(ShootEffect(self.model.fire_colour, target.rect.center, self.rect.center, 2, screen.get_size()))
                if target.health <= 0:
                    target.is_dead = True
                    pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=target))
                self.last_fired = 0

