import pygame
import random

class Field:
    # Field constants
    FIELD_WIDTH = 25
    FIELD_HEIGHT = 25
    TILE_SIZE = 32
    SHEET_ROWS = 16
    SHEET_COLS = 2

    TILLED_SOIL_FRAME = 4
    TURNIP_SEED_FRAME =  6
    TURNIP_FRAME_0 =     8 
    TURNIP_FRAME_1 =    10
    ROCK_FRAME =        42
    WEED_FRAME =        43

    NO_ITEM =     -1
    ROCK_ITEM =    0
    WEED_ITEM =    1
    TURNIP_ITEM =  2
    DROP_SUCCESS = 9

    HOUSE_TILES = []
    BIN_TILES = []

    ITEM_VALUES = {
        ROCK_ITEM :     1,
        WEED_ITEM :     1,
        TURNIP_ITEM : 100
    }

    GROWTH_THRESHOLDS = {
        TURNIP_SEED_FRAME  : 1,
        TURNIP_FRAME_0     : 2,
        TURNIP_FRAME_1     : -1,
    }

    # Field variables
    screen = None
    ground_tiles = []
    ground_growths = []
    spritesheet = None
    reticle_sprite = None
    bin_sprite = None
    house_sprite = None
    screen_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    tile_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    reticle_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    bin_rect = None
    house_rect = None

    shipped_amount = 0

    def __init__(self, s):
        self.screen = s
        for house_x in range(0,8):
            for house_y in range(0,6):
                self.HOUSE_TILES.append((house_x, house_y))

        for bin_x in range(8,10):
            for bin_y in range(4,6):
                self.BIN_TILES.append((bin_x, bin_y))

        for x in range(0, self.FIELD_WIDTH):
            field_row = []
            growth_row = []
            for y in range(0, self.FIELD_HEIGHT):
                rand_spawn = random.randint(0, 20)
                if rand_spawn == 0:
                    field_row.append(self.ROCK_FRAME)
                elif rand_spawn == 1:
                    field_row.append(self.WEED_FRAME)
                else:
                    field_row.append(random.randint(0,3))
                growth_row.append(0)
            self.ground_tiles.append(field_row)
            self.ground_growths.append(growth_row)
        self.spritesheet = pygame.image.load("field-big.png")
        self.reticle_sprite = pygame.image.load("reticle-big.png")

        self.bin_sprite = pygame.image.load("bin-big.png").convert_alpha()
        self.bin_rect = self.bin_sprite.get_rect()
        self.bin_rect.topleft = (256, 122)

        self.house_sprite = pygame.image.load("house-big.png").convert_alpha()
        self.house_rect = self.house_sprite.get_rect()
        self.house_rect.topleft = (16, 16)

        self.till_tile(5, 5)

    def set_reticle_pos(self, tile_x, tile_y):
        if tile_x < 0:
            tile_x = 0
        elif tile_x > self.FIELD_WIDTH:
            tile_x = self.FIELD_WIDTH

        if tile_y < 0:
            tile_y = 0
        elif tile_y > self.FIELD_HEIGHT:
            tile_y = self.FIELD_HEIGHT

        self.reticle_rect.topleft = (self.TILE_SIZE * tile_x, self.TILE_SIZE * tile_y)

    def till_tile(self, tile_x, tile_y):
        if self.ground_tiles[tile_x][tile_y] <= 3:
            self.ground_tiles[tile_x][tile_y] = self.TILLED_SOIL_FRAME

    def sow_tile(self, tile_x, tile_y):
        # Sow seeds in 3x3 grid
        for y in range(-1, 2):
            for x in range(-1, 2):
                cur_x = tile_x + x
                cur_y = tile_y + y

                # Check if tiles are within bounds, only modify tilled soil
                if (cur_x >= 0 and cur_x < self.FIELD_WIDTH
                    and cur_y >= 0 and cur_y < self.FIELD_HEIGHT
                    and (self.ground_tiles[cur_x][cur_y] == self.TILLED_SOIL_FRAME
                        or self.ground_tiles[cur_x][cur_y] == self.TILLED_SOIL_FRAME + 1)):
                    # Modulo operation is used to retain watered state
                    self.ground_tiles[cur_x][cur_y] = self.TURNIP_SEED_FRAME + (self.ground_tiles[cur_x][cur_y] % 2)

    def water_tile(self, tile_x, tile_y):
        print("WATER TILE: "+str(tile_x)+", "+str(tile_y))
        if self.ground_tiles[tile_x][tile_y] > 3 and self.ground_tiles[tile_x][tile_y] % 2 == 0:
            self.ground_tiles[tile_x][tile_y] += 1

    def use_tile(self, tile_x, tile_y):
        if (tile_x, tile_y) in self.HOUSE_TILES:
            print("SLEEPING TIME")
            self.next_day()
            return self.NO_ITEM
        elif self.ground_tiles[tile_x][tile_y] == self.ROCK_FRAME:
            self.ground_tiles[tile_x][tile_y] = random.randint(0,3)
            return self.ROCK_ITEM
        elif self.ground_tiles[tile_x][tile_y] == self.WEED_FRAME:
            self.ground_tiles[tile_x][tile_y] = random.randint(0,3)
            return self.WEED_ITEM
        elif self.ground_tiles[tile_x][tile_y] == self.TURNIP_FRAME_1:
            self.ground_tiles[tile_x][tile_y] = random.randint(0,3)
            return self.TURNIP_ITEM
        
        return self.NO_ITEM
        
    def drop_item(self, tile_x, tile_y, item_type):
        if (tile_x, tile_y) in self.BIN_TILES:
            self.shipped_amount += self.ITEM_VALUES[item_type]
            print("SHIPPED CROP! Total: "+str(self.shipped_amount))

            return self.DROP_SUCCESS
        elif self.ground_tiles[tile_x][tile_y] > 5:
            return self.NO_ITEM
        else:
            if item_type == self.ROCK_ITEM:
                self.ground_tiles[tile_x][tile_y] = self.ROCK_FRAME
            elif item_type == self.WEED_ITEM:
                self.ground_tiles[tile_x][tile_y] = self.WEED_FRAME

            return self.DROP_SUCCESS
        
    def next_day(self):
        for y in range(0, self.FIELD_HEIGHT):
            for x in range(0, self.FIELD_WIDTH):

                if (self.ground_tiles[x][y] >= self.TURNIP_SEED_FRAME
                    and self.ground_tiles[x][y] <= self.TURNIP_FRAME_1):
                    print("TURNIP TILE: "+str(x)+", "+str(y))
                    # Increase growth of crops if watered
                    if self.ground_tiles[x][y] % 2 == 1:
                        self.ground_growths[x][y] += 1
                        if self.GROWTH_THRESHOLDS[self.ground_tiles[x][y] - 1] != -1:
                            if self.ground_growths[x][y] >= self.GROWTH_THRESHOLDS[self.ground_tiles[x][y] - 1]:
                                self.ground_growths[x][y] = 0
                                self.ground_tiles[x][y] += 1
                            # Reset watered state
                            else:
                                self.ground_tiles[x][y] -= 1
                        else:
                            self.ground_tiles[x][y] -= 1
                elif (self.ground_tiles[x][y] == self.TILLED_SOIL_FRAME + 1):
                    self.ground_tiles[x][y] = self.TILLED_SOIL_FRAME

    def draw(self):
        for y in range(0, self.FIELD_HEIGHT):
            for x in range(0, self.FIELD_WIDTH):
                self.screen_rect.topleft = (x * self.TILE_SIZE, y * self.TILE_SIZE)
                cur_row = self.ground_tiles[x][y] // (self.SHEET_COLS)
                cur_col = self.ground_tiles[x][y] % self.SHEET_COLS

                self.tile_rect.topleft = (self.TILE_SIZE * cur_col, self.TILE_SIZE * cur_row)
                self.screen.blit(self.spritesheet, self.screen_rect, self.tile_rect)
                self.screen.blit(self.reticle_sprite, self.reticle_rect)

        self.screen.blit(self.house_sprite, self.house_rect)
        self.screen.blit(self.bin_sprite, self.bin_rect)