import pygame
from settings import Settings


class Level():
    """Description Goes here

    Attributes:

    """

    def __init__(self, data, settings):
        self.tile_list = []
        self.settings = settings
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
                    color = (0, 0, 0)
                    tile = (color, pygame.Rect((x, y), (self.settings.tile_size, self.settings.tile_size)))
                    self.tile_list.append(tile)
                if tile == 2:
                    pass
                col_count += 1
            row_count += 1

    def draw(self, screen):
        """Description Goes here

        Args:

        Returns:
        """

        for tile in self.tile_list:
            pygame.draw.rect(screen, tile[0], tile[1])
