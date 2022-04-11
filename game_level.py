import pygame
from settings import Settings
import time
import copy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Level(Settings):
    """The Level class is used to draw and add the level object
    data onto the screen.

    Attributes: 
        data: a list of numbers representing different tiles.

    """

    def __init__(self, data):
        super().__init__()
        self.tile_list = []
        self.input_data = copy.deepcopy(data)
        print(self.input_data)
        self.data = data
        self.coins = 0
    

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    color = BLACK
                    tile = (color, pygame.Rect((x, y), (self.tile_size, self.tile_size)))
                    self.tile_list.append(tile)
                if tile == 2:
                    radius = self.tile_size//2
                    x = col_count * self.tile_size
                    y = row_count * self.tile_size
                    center = (x+radius, y+radius)
                    color = YELLOW
                    tile = [color, center, radius, self.bg_color, pygame.Rect(
                        (x, y), (self.tile_size, self.tile_size)),col_count,row_count]
                    self.tile_list.append(tile)
                    self.coins += 1
                col_count += 1
            row_count += 1

    def draw(self, screen):
        """Draws the tiles onto the game screen

        Args:
            screen: Pygame display object

        """

        for tile in self.tile_list:
            if tile[0] == BLACK:
                pygame.draw.rect(screen, tile[0], tile[1])
            elif tile[0] == YELLOW:
                pygame.draw.rect(screen, tile[3], tile[4])
                pygame.draw.circle(screen, tile[0], tile[1], tile[2])

    def get_max_coins(self):
        return self.coins
