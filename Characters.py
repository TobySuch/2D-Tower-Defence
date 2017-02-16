import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, sprie_sheet_name, sprite_width, sprite_height):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.images = []
        self.load_spritesheet(sprie_sheet_name, sprite_width, sprite_height)

    def move(self, dx=0, dy=0):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def load_spritesheet(self, file_name, sprite_width, sprite_height):
        sheet = pygame.image.load("/assets/" + file_name).convert()
        for y in range(0, sheet.height, sprite_height):
            for x in range(0, sheet.width, sprite_width):
                sprite = pygame.Surface((sprite_width, sprite_height))
                sprite.blit(sheet, (x, y), pygame.Rect(x, y, sprite_width, sprite_height))
                self.images.append(sprite)


class Player(Character):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos


class Enemy(Character):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos