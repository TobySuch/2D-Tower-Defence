import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.text = text
        self.__background_colour = background_colour
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def background_colour(self):
        return self.__background_colour

    @background_colour.setter
    def background_colour(self, colour):
        self.__background_colour = colour
        self.create_image()

    def contains(self, point):
        """Used to test if the mouse clicked on the button"""
        return self.rect.collidepoint(point)

    def create_image(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.background_colour)

        # Write the text to the button
        font = pygame.font.SysFont("Arial", self.text_size)
        text_surf = font.render(self.text, 1, self.text_colour)
        self.image.blit(text_surf, (self.rect.width / 2 - text_surf.get_width() / 2,
                                    self.rect.height / 2 - text_surf.get_height() / 2))
