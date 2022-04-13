import pygame


class SpriteSheet():
    """Description Goes here

    Attributes:

    """

    def __init__(self, filename, scale_factor=6.8*1.25):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.scale_factor = scale_factor
        self.sheetsize = self.sheet.get_rect()
        self.sheet_rows = 8
        self.sheet_columns = 9
        self.img_width = self.sheetsize.w / self.sheet_columns
        self.img_height = self.sheetsize.h / self.sheet_rows

    def get_image(self, x, y, width, height):
        """Gets an image from the selected area of a file.

        Args:
            x: 
            y:
            width:
            height:

        Returns:

        """

        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/self.scale_factor, height/self.scale_factor))
        return image

    def get_image_hflip(self, x, y, width, height):
        """Gets a mirrored image from the selected area of a file.

        Args:

        Returns:

        """

        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/self.scale_factor, height/self.scale_factor))
        image = pygame.transform.flip(image, True, False)
        return image
