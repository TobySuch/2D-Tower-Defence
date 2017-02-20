from Lib import *


class ShootEffect(pygame.sprite.Sprite):
    def __init__(self, colour, startpos, endpos, timeout, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.startpos = startpos
        self.endpos = endpos
        self.timeout = timeout
        self.image = pygame.Surface(screen_size, pygame.SRCALPHA)
        pygame.draw.line(self.image, self.colour, self.startpos, self.endpos, 3)
        self.rect = self.image.get_rect()
        self.time_alive = 0

    def update(self):
        self.time_alive += 1
        if self.time_alive > self.timeout:
            self.kill()


class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_location):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.sprite_location = sprite_location
        self.images = []
        self.load_spritesheet(GRID_SIZE, GRID_SIZE)
        self.time_alive = 0
        self.image = self.images[self.time_alive]
        self.rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))


    def load_spritesheet(self, sprite_width, sprite_height):
        sheet = pygame.image.load("assets/" + self.sprite_location).convert()
        for y in range(0, sheet.get_height(), sprite_height):
            for x in range(0, sheet.get_width(), sprite_width):
                sprite = pygame.Surface((sprite_width, sprite_height))
                sprite.blit(sheet, (0, 0), pygame.Rect(x, y, sprite_width, sprite_height))
                self.images.append(sprite)

    def update(self):
        self.time_alive += 1
        if self.time_alive >= len(self.images):
            self.kill()


