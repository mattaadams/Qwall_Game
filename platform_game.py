import pygame
import sys
from animation import SpriteSheet
from settings import Settings
from game_level import Level
import time
# Issues: Can pause in main menu
# Roadmap:
# Add ending after collection of all circles
# Add leaderboard
# Randomize coin appearances -- (* Tiles)
# Hazardous blocks
# Agent AI

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class PlatformGame():
    """Description Goes here

    Attributes:

    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Platform Game')
        self.settings = Settings()
        self.level = Level(level_data, self.settings)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.player = Player(self.level, 50, 882)
        self.run = True
        self.menu = True
        self.paused = False
        self.pause_total = 0

    def main_menu(self):
        """Renders a main menu screen"""
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.menu = False
            self.screen.fill(self.settings.menu_color)
            font = pygame.font.Font(None, 120)
            text = font.render("Press Any Key to Start!", True, BLACK)
            text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
            self.screen.blit(text, text_rect)
            self.menu_duration = pygame.time.get_ticks() // 1000
            pygame.display.update()

    def pause_screen(self):
        """Renders a main pause screen"""
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and self.paused == False and self.menu == False:
            self.paused = True
            pause_start_time = pygame.time.get_ticks()
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.paused = False
                    self.pause_total += (pygame.time.get_ticks() - pause_start_time) // 1000
            pause_bg = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            pause_bg.set_alpha(10)
            pause_bg.fill((220, 220, 220))
            self.screen.blit(pause_bg, (0, 0))
            font = pygame.font.Font(None, 120)
            text = font.render("PAUSED", True, BLACK)
            text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def run_game(self):
        """Runs the game by calling the functions to generate the environment"""
        while self.run:
            self.clock.tick(27)
            self.main_menu()
            self.pause_screen()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.player.move(self.screen)

    def _update_screen(self):
        game_time = (pygame.time.get_ticks() // 1000)
        base_score = 100 - game_time + self.menu_duration + self.pause_total
        score = self.player.score + base_score
        self.screen.fill(self.settings.bg_color)
        self.level.draw(self.screen)
        self.draw_grid()
        font = pygame.font.Font(None, 48)
        text = font.render(f'Score: {score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(90, 25))
        self.screen.blit(text, text_rect)
        self.player.draw(self.screen)
        pygame.display.update()

    def draw_grid(self):
        """Description Goes here

        Args:

        Returns:

        """

        grid_range = self.settings.screen_width // self.settings.tile_size
        for line in range(0, grid_range):
            pygame.draw.line(
                self.screen, WHITE,
                (0, line * self.settings.tile_size),
                (self.settings.screen_width, line * self.settings.tile_size))
            pygame.draw.line(
                self.screen, WHITE,
                (line * self.settings.tile_size, 0),
                (line * self.settings.tile_size, self.settings.screen_width))


class Player():
    """Description Goes here

    Attributes:
        level: A `Level` object
        x: An integer
        y: An integer
        width: An integer
        height: An integer

    """

    def __init__(self, level, x, y, width=26, height=50, settings=Settings()):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_y = 10
        self.vel_x = 10
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.sprite_sheet = SpriteSheet('assets/stick_man_blue.png')
        self.scale_factor = self.sprite_sheet.scale_factor
        self.scaled_width = self.width * self.scale_factor
        self.scaled_height = self.height * self.scale_factor
        self.frame = 0
        self.settings = settings
        self.level = level
        self.score = 0

    def draw(self, win):
        """Description Goes here

        Args:
            win: Pygame display object

        Returns:

        """

        image_right = self.sprite_sheet.get_image(
            self.scaled_width*self.frame, self.scaled_height*self.frame, self.scaled_width, self.scaled_height)
        image_left = self.sprite_sheet.get_image_hflip(
            self.scaled_width*self.frame, self.scaled_height*self.frame, self.scaled_width, self.scaled_height)

        if self.walkCount + 1 >= 21:
            self.walkCount = 0
        if self.left:
            win.blit(image_left, (self.x, self.y))
            self.walkCount += 1
            self.frame = self.walkCount//3
        elif self.right:
            win.blit(image_right, (self.x, self.y))
            self.walkCount += 1
            self.frame = self.walkCount//3
        else:
            win.blit(self.sprite_sheet.get_image(0, 0, self.scaled_width,
                     self.scaled_height), (self.x, self.y))

    def move(self, win):
        """Description Goes here

        Args:

        Returns:

        """
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.vel_x:
            dx -= self.vel_x
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x < self.settings.screen_width - self.width - self.vel_x:
            dx += self.vel_x
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.walkCount = 0

        if keys[pygame.K_SPACE] and self.isJump == False and self.vel_y == 0:
            self.vel_y = -15
            self.isJump = True

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in self.level.tile_list:
            if tile[0] == BLACK:
                if tile[1].colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.x, self.y + dy, self.width, self.height):

                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.y
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - (self.y+self.height)
                        self.vel_y = 0
                        self.isJump = False
                if self.y < 0:
                    dy = 0 - self.y
                    self.vel_y = 0
            elif tile[0] == YELLOW:
                if tile[4].colliderect(self.x, self.y, self.width, self.height):
                    self.score += 1
                    tile[0] = self.settings.bg_color

            else:
                pass

        self.x += dx
        self.y += dy


# Level data size = (tile_size/width,tile_size/height)
# each element represents a tile
level_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

platform_game = PlatformGame()
platform_game.run_game()
