import pygame
import sys
from animation import SpriteSheet
from settings import Settings
from game_level import Level
import numpy as np

# Todo:
# Check state input, what should be included 
# rewards for collisision, 
# improving model, add layers and others stuf



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class PlatformGameAI(Settings):
    """PlatformGame class is used to update the screen 
    and check events while the game is running.

    Attributes:
    
    """

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Platform Game')
        self.level = Level(level_data)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.player = Player(self.level, 40, 720)
        self.game_score = 30
        self.restart_time = 0

    def reset(self):
        self.__init__()
        self.restart_time = (pygame.time.get_ticks() // 1000)


    def play_event(self,action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.player.move(action)
        last_score = self.game_score
        game_time = (pygame.time.get_ticks() // 1000)
        base_score = 25 - game_time  + self.restart_time
        self.game_score = self.player.coins*3 + base_score
        self._update_screen()
        self.clock.tick(27)
        game_over = False
        if self.game_score == 0:
            game_over = True
            reward = -10

        if (self.game_score - last_score) > 0: 
            reward = 3
        else: 
            reward = -1
            
        return reward, game_over, self.game_score

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.level.draw(self.screen)
        self._draw_grid()
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.game_score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(60, 16))
        self.screen.blit(text, text_rect)
        self.player.draw(self.screen)
        pygame.display.update()
        

    def _draw_grid(self):
        grid_range = self.screen_width // self.tile_size
        for line in range(0, grid_range):
            pygame.draw.line(
                self.screen, WHITE,
                (0, line * self.tile_size),
                (self.screen_width, line * self.tile_size))
            pygame.draw.line(
                self.screen, WHITE,
                (line * self.tile_size, 0),
                (line * self.tile_size, self.screen_width))


class Player(Settings):
    """The Player Class represents a player inside the game.

    Attributes:
        level: A `Level` object
        x: An integer
        y: An integer
        width: An integer
        height: An integer

    """

    def __init__(self, level, x, y, width=21, height=40):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_y = 0
        self.vel_x = 8
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.sprite_sheet = SpriteSheet('assets/stick_man_blue.png')
        self.scale_factor = self.sprite_sheet.scale_factor
        self.scaled_width = self.width * self.scale_factor
        self.scaled_height = self.height * self.scale_factor
        self.frame = 0
        self.level = level
        self.coins = 0

    def draw(self, win):
        """Creates a drawing of the player object on the game screen

        Args:
            win: Pygame display object
        
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


    def move(self, action):
        """Moves the position of the player object."""
        dx = 0
        dy = 0
        # [Left, Right, Stop, Jump]
        if np.array_equal(action, [1, 0, 0, 0]) and self.x > self.vel_x:
            dx -= self.vel_x
            self.left = True
            self.right = False
        if np.array_equal(action, [0, 1, 0, 0]) and self.x < self.screen_width - self.width - self.vel_x:
            dx += self.vel_x
            self.left = False
            self.right = True
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.left = False
            self.right = False
            self.walkCount = 0

        if np.array_equal(action, [0, 0, 0, 1]) and self.isJump == False and self.vel_y == 0:
            self.vel_y = -14
            self.isJump = True

        self.vel_y += 1
        if self.vel_y > 8:
            self.vel_y = 8
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
                    self.coins += 1
                    tile[0] = self.bg_color
                    self.level.data[tile[6]][tile[5]] = 0

            else:
                pass

        self.x += dx
        self.y += dy


# Level data size = (tile_size/width,tile_size/height)
# each element represents a tile
level_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 2, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


#platform_game = PlatformGameAI()
#platform_game.run_game()
