import pygame


idle = pygame.image.load('assets/standing.png')

walkRight = [
    pygame.image.load('assets/R1.png'),
    pygame.image.load('assets/R2.png'),
    pygame.image.load('assets/R3.png'),
    pygame.image.load('assets/R4.png'),
    pygame.image.load('assets/R5.png'),
    pygame.image.load('assets/R6.png'),
    pygame.image.load('assets/R7.png'),
    pygame.image.load('assets/R8.png'),
    pygame.image.load('assets/R9.png')]

walkLeft = [
    pygame.image.load('assets/L1.png'),
    pygame.image.load('assets/L2.png'),
    pygame.image.load('assets/L3.png'),
    pygame.image.load('assets/L4.png'),
    pygame.image.load('assets/L5.png'),
    pygame.image.load('assets/L6.png'),
    pygame.image.load('assets/L7.png'),
    pygame.image.load('assets/L8.png'),
    pygame.image.load('assets/L9.png')]


class SpriteSheet:

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/5, height/5))
        return image

    def get_image_hflip(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/5, height/5))
        image = pygame.transform.flip(image, True, False)
        return image
