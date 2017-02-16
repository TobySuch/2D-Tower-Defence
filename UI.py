import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour):
        pygame.sprite.Sprite.__init__(self)
        self.background_colour = background_colour
        self.text_colour = text_colour
        self.text = text
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(background_colour)
        self.rect = rect

        # Write the text to the button
        font = pygame.font.SysFont("Arial", 100)
        text_surf = font.render(text, 1, text_colour)
        self.image.blit(text_surf, (self.rect.width/2 - text_surf.get_width()/2,
                        self.rect.height/2 - text_surf.get_height()/2))

    def contains(self, point):
        """Used to test if the mouse clicked on the button"""
        return self.rect.collidepoint(point)
