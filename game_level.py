import pygame
from settings import Settings
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Level():
    """Description Goes here

    Attributes:

    """

    def __init__(self, data, settings):
        self.tile_list = []
        self.settings = settings
        self.data = data
        self.coins = 0
        # load images
        # dirt_img = pygame.image.load('img/dirt.png')
        # grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    x = col_count * self.settings.tile_size
                    y = row_count * self.settings.tile_size
                    color = BLACK
                    tile = (color, pygame.Rect((x, y), (self.settings.tile_size, self.settings.tile_size)))
                    self.tile_list.append(tile)
                if tile == 2:
                    radius = self.settings.tile_size//2
                    x = col_count * self.settings.tile_size
                    y = row_count * self.settings.tile_size
                    center = (x+radius, y+radius)
                    color = YELLOW
                    tile = [color, center, radius, self.settings.bg_color, pygame.Rect(
                        (x, y), (self.settings.tile_size, self.settings.tile_size))]
                    self.tile_list.append(tile)
                    self.coins += 1
                col_count += 1
            row_count += 1

    def draw(self, screen):
        """Description Goes here

        Args:

        Returns:
        """

        for tile in self.tile_list:
            if tile[0] == BLACK:
                pygame.draw.rect(screen, tile[0], tile[1])
            elif tile[0] == YELLOW:
                pygame.draw.rect(screen, tile[3], tile[4])
                pygame.draw.circle(screen, tile[0], tile[1], tile[2])

    def get_max_coins(self):
        return self.coins
