import pygame
from animation import idle, walkLeft, walkRight
pygame.init()


clock = pygame.time.Clock()
tile_size = 50
win_x = 1200
win_y = 720
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Untitled Platform Game")

bg = pygame.image.load('Background.jpg')
bg = pygame.transform.scale(bg, (1280, 720))


def draw_grid():
    for line in range(0, 24):
        pygame.draw.line(win, (255, 255, 255), (0, line * tile_size), (win_x, line * tile_size))
        pygame.draw.line(win, (255, 255, 255), (line * tile_size, 0), (line * tile_size, win_x))


class Player():
    def __init__(self, x, y, width, height):
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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(idle, (self.x, self.y))


man = Player(300, 600, 64, 64)


def redrawGameWindow():
    global walkCount
    win.blit(bg, (0, 0))
    man.draw(win)
    draw_grid()
    pygame.display.update()


run = True

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < win_x - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
    else:
        man.left = False
        man.right = False
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.3
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
