import pygame

class Player:
    # State consts
    IDLE_STATE = 0
    MOVING_STATE = 1
    USING_STATE = 2

    WALK_SPEED = 3
    RUN_SPEED = 6

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)

    # Animations
    IDLE_ANIMATION = [(0, 60)]
    WALK_ANIMATION = [(0, 10), (1, 10), (0, 10), (2, 10)]
    RUN_ANIMATION = [(0, 8), (3, 8), (0, 8), (4, 8)]
    TILLING_ANIMATION = [(12, 15), (13, 4), (14, 8), (15, 30)]

    # Variables
    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    current_frame = 0
    current_animation = None

    frame_counter = 0
    current_duration = 0
    animation_index = 0

    running = False

    screen_rect = None
    frame_rect = None

    spritesheet = None

    def __init__(self):
        self.spritesheet = pygame.image.load("farmer-big.png").convert_alpha()
        self.frame_rect = pygame.Rect(0, 0, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect = pygame.Rect(self.pos_x, self.pos_y, self.FRAME_SIZE[0], self.FRAME_SIZE[1])
        self.screen_rect.center = (self.pos_x, self.pos_y)
        self.set_animation(self.IDLE_ANIMATION)

    def set_frame(self, frame):
        self.current_frame = frame
        cur_row = self.current_direction
        cur_col = self.current_frame

        self.frame_rect.topleft = (cur_col * self.FRAME_SIZE[0], cur_row * self.FRAME_SIZE[1])

    def next_frame(self):
        self.current_frame = self.current_animation[self.animation_index][0]
        self.current_duration = self.current_animation[self.animation_index][1]

    def set_animation(self, animation):
        self.current_animation = animation
        self.animation_index = 0

        self.frame_counter = 0
        self.next_frame()
        self.set_frame(self.current_frame)

    def update_animation(self):
        self.frame_counter += 1

        if self.frame_counter >= self.current_duration:
            self.frame_counter = 0
            self.animation_index += 1
            if self.animation_index >= len(self.current_animation):
                self.animation_index = 0
                if self.current_state == self.USING_STATE:
                    self.current_state = self.IDLE_STATE
                    self.set_animation(self.IDLE_ANIMATION)
                    return
            self.next_frame()
            self.set_frame(self.current_frame)

    def use_tool(self):
        self.current_state = self.USING_STATE
        self.set_animation(self.TILLING_ANIMATION)

    def move(self, direction):
        if self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE:
            return

        if self.current_state != self.MOVING_STATE:
            if self.running:
                self.set_animation(self.RUN_ANIMATION)
            else:
                self.set_animation(self.WALK_ANIMATION)
            self.current_state = self.MOVING_STATE

        if self.running == True:
            if direction == self.DOWN:
                self.pos_y += self.RUN_SPEED
                self.current_direction = self.DOWN
            if direction == self.UP:
                self.pos_y -= self.RUN_SPEED
                self.current_direction = self.UP
            if direction == self.LEFT:
                self.pos_x -= self.RUN_SPEED
                self.current_direction = self.LEFT
            if direction == self.RIGHT:
                self.pos_x += self.RUN_SPEED
                self.current_direction = self.RIGHT
        else:
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

    def stop_move(self):
        if self.current_state == self.MOVING_STATE:
            self.current_state = self.IDLE_STATE
            self.set_animation(self.IDLE_ANIMATION)

    def start_running(self):
        self.running = True
        if self.current_animation != self.RUN_ANIMATION:
            self.set_animation(self.RUN_ANIMATION)

    def stop_running(self):
        self.running = False
        if self.current_state == self.MOVING_STATE:
            self.set_animation(self.WALK_ANIMATION)

    def update(self):
        self.update_animation()

    def draw(self, screen):
        screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)