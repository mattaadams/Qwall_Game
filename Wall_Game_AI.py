import pygame
import sys
from animation import SpriteSheet
from settings import Settings
from game_level import Level
import numpy as np
from collections import deque
from PIL import Image
import cv2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class WallGameAI(Settings):
    """WallGame class is used to update the screen
    and check events while the game is running.

    Attributes:

    """

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Wall Game')
        self.level = Level(level_data)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.SIZE = 12
        self.ACTION_SPACE_SIZE = 3
        self.OBSERVATION_SPACE_VALUES = (self.SIZE, self.SIZE, 3)
        self.PLAYER_N = 3  # player key in dict
        self.player = Player(self.level, 40, 320)
        self.game_score = 0
        self.d = {0: (0, 0, 0),
                  1: (255, 255, 255),
                  2: (0, 255, 255),
                  3: (0, 0, 255)}

    def reset(self):
        self.episode_step = 0
        state = np.array(self.get_image())
        self.level = Level(level_data)
        self.wall = Wall(self.level)
        self.player = Player(self.level, 40, 320)
        self.game_score = 0
        return state

    def step(self, action):
        self.episode_step += 1
        reward = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game_over = self.player.move(action)
        self.wall.move()
        if self.wall.x <= self.wall.speed:
            self.game_score += 1
            reward = 1
        new_state = np.array(self.get_image())
        self._update_screen()
        self.clock.tick(27)
        if game_over == True:
            reward = -10
            self.reset()

        return new_state, reward, game_over

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.level.draw(self.screen)
        self._draw_grid()
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.game_score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(60, 20))
        self.screen.blit(text, text_rect)
        self.wall.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.update()

    def _draw_grid(self):
        dim = max(self.screen_height, self.screen_width)
        grid_range = dim // self.tile_size
        for line in range(0, grid_range):
            pygame.draw.line(
                self.screen, WHITE,
                (0, line * self.tile_size),
                (dim, line * self.tile_size))
            pygame.draw.line(
                self.screen, WHITE,
                (line * self.tile_size, 0),
                (line * self.tile_size, dim))

    def get_image(self):
        """Gets an image representation of our state to be used
        by the Deep-Q Network
        """
        env = np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8)  # starts an rbg of our size
        for i, row in enumerate(self.level.data):
            for j, col in enumerate(self.level.data):
                env[i][j] = self.d[self.level.data[i][j]]
        # sets the player tile to red
        env[self.player.y//self.tile_size][self.player.x//self.tile_size] = self.d[self.PLAYER_N]
        img = Image.fromarray(env, 'RGB')
        return img

    def render(self):
        """Resizes and displays the image so we can view the state
        """
        img = self.get_image()
        img = img.resize((300, 300))
        cv2.imshow("image", np.array(img))
        cv2.waitKey(5)


class Player(Settings):
    """The Player Class represents a player inside the game.

    Attributes:
        level: A `Level` object
        x: An integer representing player's x-coordinate
        y: An integer representing player's y-coordinate
        width: An integer representing player's width
        height: An integer representing player's height

    """

    def __init__(self, level, x, y, width=40, height=40):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_y = 40
        self.up = False
        self.down = False
        self.level = level
        self.coins = 0

    def draw(self, win):
        """Creates a drawing of the player object on the game screen

        Args:
            win: Pygame display object

        """
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def move(self, action):
        """Moves the position of the player object."""
        game_over = False
        dy = 0

        if action == 0 and self.y > 0:
            dy -= self.vel_y
            self.up = True
            self.down = False
        elif action == 1 and self.y < self.screen_height - self.height:
            dy += self.vel_y
            self.up = False
            self.down = True
        elif action == 2:
            self.up = False
            self.down = False

        for tile in self.level.tile_list:
            if tile[0] == BLACK:
                if tile[1].colliderect(self.x, self.y, self.width, self.height):
                    game_over = True

            elif tile[0] == YELLOW:
                if tile[4].colliderect(self.x, self.y, self.width, self.height):
                    self.coins += 1
                    tile[0] = self.bg_color
                    self.level.data[tile[6]][tile[5]] = 0
            else:
                continue

        self.y += dy
        return game_over


class Wall(Settings):
    """The Wall Class represents a player inside the game.

    Attributes:
        level: A `Level` object
        x: An integer representing player's x-coordinate
        y: An integer representing player's y-coordinate
        width: An integer representing player's width
        height: An integer representing player's height

    """

    def __init__(self, level):
        super().__init__()
        self.x = self.screen_width
        self.y = 0
        self.level = level
        self.speed = 20
        self.hole_size = 4
        self.hole_position = 4
        self.body = np.ones((1, self.screen_height//self.tile_size))

    def draw(self, win):
        """Creates a drawing of the wall object on the game screen

        Args:
            win: Pygame display object

        """
        self.level.data = np.zeros((12, 12))
        self.level.data[:, (self.x-1)//self.tile_size] = 1
        a = self.hole_position
        b = self.hole_size
        self.level.data[a:a+b, (self.x-1)//self.tile_size] = 0
        if self.x <= self.speed:
            self.hole_size, self.hole_position = self.create_hole()
            self.x = self.screen_width

    def move(self):
        """Moves the position of the wall object."""
        self.x -= self.speed

    def create_hole(self):
        self.hole_size = np.random.randint(2, 6)
        self.hole_position = np.random.randint(0, 11)
        return self.hole_size, self.hole_position


level_data = np.zeros((12, 12))
