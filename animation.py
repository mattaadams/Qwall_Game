import pygame


class SpriteSheet():
    """Description Goes here

    Attributes:

    """

    def __init__(self, filename, scale_factor=6.8):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.scale_factor = scale_factor
        self.sheetsize = self.sheet.get_rect()
        self.sheet_rows = 8
        self.sheet_columns = 9
        self.img_width = self.sheetsize.w / self.sheet_columns
        self.img_height = self.sheetsize.h / self.sheet_rows

    def get_image(self, x, y, width, height):
        """Description Goes here

        Args:

        Returns:

        """

        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/self.scale_factor, height/self.scale_factor))
        return image

    def get_image_hflip(self, x, y, width, height, scale_factor=6.8):
        """Description Goes here

        Args:

        Returns:

        """

        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((x, y, width, height)))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (width/self.scale_factor, height/self.scale_factor))
        image = pygame.transform.flip(image, True, False)
        return image
#################to-do##############

    # def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
    #                      y_margin=0, y_padding=0):

    #     sheet_rect = self.sheet.get_rect()
    #     sheet_width, sheet_height = sheet_rect.size

    #     x_sprite_size = (sheet_width - 2 * x_margin
    #                      - (num_cols - 1) * x_padding) / num_cols
    #     y_sprite_size = (sheet_height - 2 * y_margin
    #                      - (num_rows - 1) * y_padding) / num_rows

    #     sprite_rects = []
    #     for row_num in range(num_rows):
    #         for col_num in range(num_cols):
    #             x = x_margin + col_num * (x_sprite_size + x_padding)
    #             y = y_margin + row_num * (y_sprite_size + y_padding)
    #             sprite_rect = (x, y, x_sprite_size, y_sprite_size)
    #             sprite_rects.append(sprite_rect)

    #     grid_images = self.images_at(sprite_rects)
    #     print(f"Loaded {len(grid_images)} grid images.")

    #     return grid_images
