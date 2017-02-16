import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheet_name, sprite_width, sprite_height):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.load_spritesheet(sprite_sheet_name, sprite_width, sprite_height)
        self.sprite_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def move(self, dx=0, dy=0):
        self.rect.topleft = (self.rect.topleft[0] + dx, self.rect.topleft[1] + dy)

    def load_spritesheet(self, file_name, sprite_width, sprite_height):
        sheet = pygame.image.load("assets/" + file_name).convert()
        for y in range(0, sheet.get_height(), sprite_height):
            for x in range(0, sheet.get_width(), sprite_width):
                sprite = pygame.Surface((sprite_width, sprite_height))
                sprite.blit(sheet, (0, 0), pygame.Rect(x, y, sprite_width, sprite_height))
                self.images.append(sprite)

    def update(self):
        print(self.sprite_index)
        self.image = self.images[self.sprite_index]
        self.sprite_index += 1
        if self.sprite_index >= len(self.images):
            self.sprite_index = self.sprite_index%len(self.images)



class Player(Character):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos


class Enemy(Character):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos