import pygame
import sys
from animation import SpriteSheet
from settings import Settings
from game_level import Level
import numpy as np
from collections import deque
from PIL import Image
import cv2

# Roadmap:
# Menu buttons (ai vs non-ai mode)
# Add leaderboard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class WallGame(Settings):
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
        self.player = Player(self.level, 40, 360)
        self.wall = Wall(self.level)
        self.run = True
        self.menu = True
        self.paused = False
        self.is_game_over = False
        self.game_score = 0
        self.SIZE = 12
        self.PLAYER_N = 3
        self.d = {0: (0, 0, 0),
                  1: (255, 255, 255),
                  2: (0, 255, 255),
                  3: (0, 0, 255)}

    def reset(self):
        """Resets the game to its original state"""
        self.level = Level(level_data)
        self.wall = Wall(self.level)
        self.player = Player(self.level, 200, 360)
        self.run = True
        self.menu = True
        self.paused = False
        self.is_game_over = False
        self.game_score = 0

    def _main_menu(self):
        """Draws a main menu screen"""
        key = pygame.key.get_pressed()
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.menu = False
            self.screen.fill(self.menu_color)
            font = pygame.font.Font(None, 64)
            text = font.render("Press 'E' to Start!", True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def _pause_screen(self):
        """Draws a pause screen and stops all in-game events"""
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and self.paused == False and self.menu == False:
            self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.paused = False
            pause_bg = pygame.Surface((self.screen_width, self.screen_height))
            pause_bg.set_alpha(10)
            pause_bg.fill((220, 220, 220))
            self.screen.blit(pause_bg, (0, 0))
            font = pygame.font.Font(None, 120)
            text = font.render("PAUSED", True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def _game_over(self):
        """Draws the ending screen and displays the player's final score"""
        font = pygame.font.Font(None, 32)
        key = pygame.key.get_pressed()
        text = font.render("GAME OVER. Press 'R' to Restart", True, BLACK)
        subtext = font.render(f"Score: {self.game_score}", True, BLACK)
        while self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.render()
                        self.reset()

            text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            subtext_rect = subtext.get_rect(center=(self.screen_width/2, 120+(self.screen_height/2)))

            self.screen.fill(self.bg_color)
            self.screen.blit(text, text_rect)
            self.screen.blit(subtext, subtext_rect)

            pygame.display.update()

    def run_game(self):
        """Runs the game by calling the functions to generate the environment"""
        while self.run:
            self.clock.tick(27)
            self._main_menu()
            self._pause_screen()
            self._game_over()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.is_game_over = self.player.move()
        if self.is_game_over == True:
            self._game_over()
        self.wall.move()
        if self.wall.x <= self.wall.speed:
            self.game_score += 1

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.level.draw(self.screen)
        self._draw_grid()
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.game_score}', True, BLUE)
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
        # creates an array representing the size of our environment
        env = np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8)
        for x, row in enumerate(self.level.data):
            for y, col in enumerate(self.level.data):
                env[x][y] = self.d[self.level.data[x][y]]
        # sets the player tile to red
        env[self.player.y//self.tile_size][self.player.x//self.tile_size] = self.d[self.PLAYER_N]
        img = Image.fromarray(env, 'RGB')
        return img

    def render(self):
        img = self.get_image()
        img = img.resize((300, 300))  # resizing so we can view the state
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
        self.vel_x = 40
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        #self.sprite_sheet = SpriteSheet('assets/stick_man_blue.png')
        #self.scale_factor = self.sprite_sheet.scale_factor
        #self.scaled_width = self.width * self.scale_factor
        #self.scaled_height = self.height * self.scale_factor
        self.frame = 0
        self.level = level
        self.coins = 0

    def draw(self, win):
        """Creates a drawing of the player object on the game screen

        Args:
            win: Pygame display object

        """
        # optional if you have spritesheet

        # image_right = self.sprite_sheet.get_image(
        #     self.scaled_width*self.frame, self.scaled_height*self.frame, self.scaled_width, self.scaled_height)
        # image_left = self.sprite_sheet.get_image_hflip(
        #     self.scaled_width*self.frame, self.scaled_height*self.frame, self.scaled_width, self.scaled_height)

        # if self.walkCount + 1 >= 21:
        #     self.walkCount = 0
        # if self.left:
        #     win.blit(image_left, (self.x, self.y))
        #     self.walkCount += 1
        #     self.frame = self.walkCount//3
        # elif self.right:
        #     win.blit(image_right, (self.x, self.y))
        #     self.walkCount += 1
        #     self.frame = self.walkCount//3
        # else:
        #     win.blit(self.sprite_sheet.get_image(0, 0, self.scaled_width,
        #              self.scaled_height), (self.x, self.y))

        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def move(self):
        """Moves the position of the player object."""
        game_over = False
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()

        # if key[pygame.K_LEFT] and self.x > 0:
        #     dx -= self.vel_x
        #     self.right = self.up = self.down = False
        #     self.left = True
        # elif key[pygame.K_RIGHT] and self.x < self.screen_width - self.width:
        #     dx += self.vel_x
        #     self.left = self.up = self.down = False
        #     self.right = True
        if key[pygame.K_UP] and self.y > 0:
            dy -= self.vel_y
            self.left = self.right = self.down = False
            self.up = True
        elif key[pygame.K_DOWN] and self.y < self.screen_height - self.height:
            dy += self.vel_y
            self.left = self.up = self.right = False
            self.down = True
        else:
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.walkCount = 0

        # if key[pygame.K_SPACE] and self.isJump == False and self.vel_y == 0:
        #     self.vel_y = -13
        #     self.isJump = True

        # self.vel_y += 1
        # if self.vel_y > 8:
        #     self.vel_y = 8
        # dy += self.vel_y

        # Checking for player colliding with other objects in the environment
        for tile in self.level.tile_list:
            if tile[0] == BLACK:
                if tile[1].colliderect(self.x, self.y, self.width, self.height):
                    dx = 0
                    game_over = True

            elif tile[0] == YELLOW:
                if tile[4].colliderect(self.x, self.y, self.width, self.height):
                    self.coins += 1
                    tile[0] = self.bg_color
                    self.level.data[tile[6]][tile[5]] = 0
            else:
                pass

        self.x += dx
        self.y += dy
        return game_over


class Wall(Settings):
    """The Wall Class represents a player inside the game.

    Attributes:
        level: A PyGame `Level` object
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

        if self.x <= 2*self.tile_size:
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
