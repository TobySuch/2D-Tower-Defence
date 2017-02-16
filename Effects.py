import pygame


class Effect(pygame.sprite.Sprite):
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