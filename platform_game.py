import pygame
import sys
from animation import SpriteSheet
from settings import Settings
from game_level import Level
# clock = pygame.time.Clock()
# win = pygame.display.set_mode((self.screen.screen_width, win_y))
# pygame.display.set_caption("Untitled Platform Game")


class PlatformGame():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Platform Game')
        self.settings = Settings()
        self.level = Level(level_data, self.settings)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.player = Player(self.level, 50, 882)

    def main_menu(self):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    menu = False
            self.screen.fill((0, 255, 155))
            font = pygame.font.Font(None, 120)
            text = font.render("Press Any Key to Start!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
            self.screen.blit(text, text_rect)
            pygame.display.update()

    def run_game(self):
        self.main_menu()
        while True:
            self.clock.tick(27)
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.player.move()

    def _update_screen(self):
        global walkCount
        self.screen.fill(self.settings.bg_color)
        self.level.draw(self.screen)
        self.draw_grid()
        self.player.draw(self.screen)
        pygame.display.update()

    def draw_grid(self):
        grid_range = self.settings.screen_width // self.settings.tile_size
        for line in range(0, grid_range):
            pygame.draw.line(
                self.screen, (255, 255, 255),
                (0, line * self.settings.tile_size),
                (self.settings.screen_width, line * self.settings.tile_size))
            pygame.draw.line(
                self.screen, (255, 255, 255),
                (line * self.settings.tile_size, 0),
                (line * self.settings.tile_size, self.settings.screen_width))


class Player():
    def __init__(self, level, x, y, width=35, height=68, settings=Settings()):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.sprite_sheet = SpriteSheet('assets/stick_man_blue.png')
        self.frame = 0
        self.settings = settings
        self.level = level

    def draw(self, win):
        image_right = self.sprite_sheet.get_image(
            self.width*self.frame*5, self.height*self.frame*5, self.width*5, self.height*5)
        image_left = self.sprite_sheet.get_image_hflip(
            self.width*self.frame*5, self.height*self.frame*5, self.width*5, self.height*5)

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
            win.blit(self.sprite_sheet.get_image(0, 0, self.width*5, self.height*5), (self.x, self.y))

    def move(self):
        vel_x = 0
        vel_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.vel:
            vel_x -= self.vel
            #self.x -= vel_x
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x < self.settings.screen_width - self.width - self.vel:
            vel_x += self.vel
            #self.x += vel_x
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.walkCount = 0

        if not(self.isJump):
            if keys[pygame.K_SPACE]:
                self.isJump = True
                self.left = False
                self.right = False
                self.walkCount = 0
        else:
            if self.jumpCount >= -10:
                print(self.jumpCount)
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.3
                print(self.y)
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

        for tile in self.level.tile_list:

            if tile[1].colliderect(self.x + vel_x, self.y, self.width, self.height):
                vel_x = 0

        self.x += vel_x


# Level data size = (tile_size/width,tile_size/height)
# each element represents a tile
level_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],


]


platform_game = PlatformGame()
platform_game.run_game()
