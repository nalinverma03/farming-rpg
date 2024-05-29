import pygame

class Player:
    # State Constants
    IDLE_STATE = 0
    MOVING_STATE = 1

    WALK_SPEED = 3

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)

    # Variables
    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    screen_rect = None
    frame_rect = None

    spritesheet = None

    def __init__(self):
        self.spritesheet = pygame.image.load("farmer-big.png").convert_alpha()
        self.frame_rect = pygame.Rect(0, 0, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect = pygame.Rect(self.pos_x, self.pos_y, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect.center = (self.pos_x, self.pos_y)

    def move(self, direction):
        self.current_state = self.MOVING_STATE

        if direction == self.DOWN:
            self.pos_y += self.WALK_SPEED
            self.current_direction = self.DOWN
        if direction == self.UP:
            self.pos_y -= self.WALK_SPEED
            self.current_direction = self.UP
        if direction == self.LEFT:
            self.pos_x -= self.WALK_SPEED
            self.current_direction = self.LEFT
        if direction == self.RIGHT:
            self.pos_x += self.WALK_SPEED
            self.current_direction = self.RIGHT

        self.screen_rect.center = (self.pos_x, self.pos_y)
        self.frame_rect.topleft = (0, self.FRAME_SIZE[1] * self.current_direction)
    
    def stop_move(self):
        pass

    def draw(self, screen):
        screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)