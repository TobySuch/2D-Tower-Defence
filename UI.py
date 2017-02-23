from Lib import *


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
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


class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, rect, text, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.__text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text):
        self.__text = new_text
        self.create_image()

    def create_image(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Create text
        font = pygame.font.SysFont("Arial", self.text_size)
        text_surf = font.render(self.text, 1, self.text_colour)
        self.image.blit(text_surf, (self.rect.width / 2 - text_surf.get_width() / 2,
                                    self.rect.height / 2 - text_surf.get_height() / 2))


class ShopButton(Button):
    def __init__(self, tower_model, pos, text_size, text_colour):
        pygame.sprite.Sprite.__init__(self)
        self.model = tower_model
        sprite = pygame.image.load(tower_model.sprite_location)
        font = pygame.font.SysFont("Arial", text_size)
        text_surf = font.render(tower_model.name, 1, text_colour)
        self.rect = pygame.Rect(pos, (text_surf.get_rect().width + sprite.get_rect().width + 10, sprite.get_rect().height + 10))
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(sprite, (0, 5))
        self.image.blit(text_surf, (sprite.get_rect().width + 10, 0))


class Shop():
    def __init__(self, screen, rect, tower_models):
        self.rect = rect
        self.image = screen.subsurface(rect)
        self.title = TextDisplay(pygame.Rect(50, 50, 300, 80), "Shop", TEXT_COLOUR, 60)
        self.tower_models = tower_models
        self.buttons = []
        self.info_popups = []
        current_y = 250
        for tower in tower_models:
            self.buttons.append(ShopButton(tower, (50, current_y), 50, TEXT_COLOUR))
            self.info_popups.append([Button(pygame.Rect(0, 500, 400, 80), "Cost: " + str(tower.value), SHOP_BACKGROUND_COLOUR, TEXT_COLOUR, 30),
                                     Button(pygame.Rect(0, 580, 400, 80), tower.description, SHOP_BACKGROUND_COLOUR, TEXT_COLOUR, 25)])
            current_y += 100

    def render(self, selected):
        mouse_pos = adjustCoordsByOffset(pygame.mouse.get_pos(), self.image.get_abs_offset())
        self.image.fill(SHOP_BACKGROUND_COLOUR)
        self.image.blit(self.title.image, self.title.rect)
        for button in self.buttons:
            self.image.blit(button.image, button.rect)
        pygame.draw.rect(self.image, MOUSE_SELECTOR_COLOUR, self.buttons[selected].rect, 2)

        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if button.contains(mouse_pos):
                popup = self.info_popups[i]
                for p in popup:
                    self.image.blit(p.image, p.rect)


    def button_pressed(self, point):
        """Returns the index of the button if one was pressed, or -1 if not"""
        for i in range(len(self.buttons)):
            if self.buttons[i].contains(point):
                return i
        return -1
