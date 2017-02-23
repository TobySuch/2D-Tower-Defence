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
        self.spritesheet = pygame.image.load(sprite_location)
        self.time_alive = self.current_image = (0, 0)
        self.image = None
        self.rect = pygame.Rect((0, 0), (GRID_SIZE, GRID_SIZE))
        self.rect.center = pos

    def update(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0),
                        pygame.Rect(self.current_image[0] * self.rect.width, self.current_image[1] * self.rect.height,
                                    self.rect.width, self.rect.height))

        if self.current_image[0] + 1 >= self.spritesheet.get_width() // self.rect.width:
            if self.current_image[1] + 1 >= self.spritesheet.get_height() // self.rect.height:
                self.kill()
            else:
                self.current_image = (0, self.current_image[1] + 1)
        else:
            self.current_image = (self.current_image[0] + 1, self.current_image[1])


