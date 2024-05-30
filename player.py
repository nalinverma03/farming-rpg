import pygame

class Player:
    # State consts
    IDLE_STATE = 0
    MOVING_STATE = 1
    USING_STATE = 2
    SWITCHING_STATE = 3
    PICKING_UP_STATE = 4

    WALK_SPEED = 3
    RUN_SPEED = 6

    NO_ITEM =     -1
    ROCK_ITEM =    0
    WEED_ITEM =    1
    TURNIP_ITEM =  2

    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    FRAME_SIZE = (100, 100)
    TOOL_FRAME_SIZE = (32, 32)
    ITEM_FRAME_SIZE = (32, 32)
    TOOL_OFFSET = (-40, -50)
    ITEM_OFFSET = (-18, -40)
    TILE_SIZE = 32

    # Tool consts
    HOE = 0
    WATERING_CAN = 1
    TURNIP_SEED = 5

    # Tool vars
    cur_tool = 0
    tools = [HOE, WATERING_CAN, TURNIP_SEED]
    tool_frame_rect = pygame.Rect(0, 0, TOOL_FRAME_SIZE[0], TOOL_FRAME_SIZE[1])
    tool_screen_rect = pygame.Rect(0, 0, TOOL_FRAME_SIZE[0], TOOL_FRAME_SIZE[1])

    # Item vars
    item_frame_rect = pygame.Rect(0, 0, ITEM_FRAME_SIZE[0], ITEM_FRAME_SIZE[1])
    item_screen_rect = pygame.Rect(0, 0, ITEM_FRAME_SIZE[0], ITEM_FRAME_SIZE[1])

    # Animations
    IDLE_ANIMATION = [(0, 60)]
    WALK_ANIMATION = [(1, 10), (0, 10), (2, 10), (0, 10)]
    RUN_ANIMATION = [(3, 8), (0, 8), (4, 8), (0, 8)]

    PICKUP_ANIMATION =    [(5, 10)]
    HOLD_ANIMATION =      [(6, 60)]
    HOLD_WALK_ANIMATION = [(6, 10), (7, 10), (6, 10), (8, 10)]
    HOLD_RUN_ANIMATION =  [(6, 8), (9, 8), (6, 8), (10, 8)]

    TILLING_ANIMATION = [(12, 15), (13, 4), (14, 8), (15, 30)]
    WATER_ANIMATION =     [(16, 15), (17, 30), (16, 7)]
    SOW_ANIMATION =       [(18, 10), (19, 10), (20, 10), (21, 10), (22, 30)]
    TOOL_SWITCH_ANIMATION = [(11, 45)]

    TILLING_FRAME = 14
    WATERING_FRAME = 17
    SOWING_FRAME = 22

    # Variables
    screen = None
    game = None

    holding = False
    held_item = None

    pos_x = 100
    pos_y = 100

    current_state = IDLE_STATE
    current_direction = DOWN

    current_frame = 0
    current_animation = None

    frame_counter = 0
    current_duration = 0
    animation_index = 0

    tile_x = 0
    tile_y = 0
    reticle_x = 0
    reticle_y = 0

    running = False

    screen_rect = None
    frame_rect = None

    spritesheet = None
    tool_sheet = None
    item_sheet = None

    def __init__(self, g, s):
        self.game = g
        self.screen = s

        self.spritesheet = pygame.image.load("farmer-big.png").convert_alpha()
        self.tool_sheet = pygame.image.load("tools-big.png").convert_alpha()
        self.item_sheet = pygame.image.load("items-big.png").convert_alpha()
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
        self.on_frame()

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
                self.on_animation_end()
            self.next_frame()
            self.set_frame(self.current_frame)

    def on_animation_end(self):
        if self.current_state == self.USING_STATE or self.current_state == self.SWITCHING_STATE:
            self.current_state = self.IDLE_STATE
            if self.holding:
                self.set_animation(self.HOLD_ANIMATION)
            else:
                self.set_animation(self.IDLE_ANIMATION)
            return
        elif self.current_animation == self.PICKUP_ANIMATION:
            self.holding = True
            self.update_held_item_rect()
            self.item_frame_rect.topleft = (self.held_item * self.ITEM_FRAME_SIZE[0], 0)

            self.set_animation(self.HOLD_ANIMATION)
            self.current_state = self.IDLE_STATE

    def next_tool(self):
        if (self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE):
            return
        self.current_state = self.SWITCHING_STATE
        self.cur_tool += 1
        if self.cur_tool >= len(self.tools):
            self.cur_tool = 0
        self.set_animation(self.TOOL_SWITCH_ANIMATION)

        self.tool_frame_rect.topleft = (self.tools[self.cur_tool] * self.TOOL_FRAME_SIZE[0], 0)
        self.tool_screen_rect.topleft = (self.pos_x + self.TOOL_OFFSET[0], self.pos_y + self.TOOL_OFFSET[1])

    def use_tool(self):
        self.current_state = self.USING_STATE
        if self.tools[self.cur_tool] == self.HOE:
            self.set_animation(self.TILLING_ANIMATION)
        elif self.tools[self.cur_tool] == self.WATERING_CAN:
            self.set_animation(self.WATER_ANIMATION)
        elif self.tools[self.cur_tool] == self.TURNIP_SEED:
            self.set_animation(self.SOW_ANIMATION)

    def use_hand(self):
        if self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE:
            return
        
        if self.holding:
            result = self.game.drop_item(self.reticle_x, self.reticle_y, self.held_item)
            if result != self.NO_ITEM:
                self.held_item = None
                self.holding = False
                self.set_animation(self.IDLE_ANIMATION)
        else:
            result = self.game.use_tile(self.reticle_x, self.reticle_y)
            print("TRY TO PICK UP: "+str(result))
            if result != self.NO_ITEM:
                self.held_item = result
                self.current_state = self.PICKING_UP_STATE
                self.set_animation(self.PICKUP_ANIMATION)

    def move(self, direction):
        if self.current_state != self.IDLE_STATE and self.current_state != self.MOVING_STATE:
            return

        if self.current_state != self.MOVING_STATE:
            if self.running:
                if self.holding:
                    self.set_animation(self.HOLD_RUN_ANIMATION)
                else:
                    self.set_animation(self.RUN_ANIMATION)
            else:
                if self.holding:
                    self.set_animation(self.HOLD_WALK_ANIMATION)
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
        self.update_tile_position()
        self.game.set_reticle_pos(self.reticle_x, self.reticle_y)

        if self.holding:
            self.update_held_item_rect()

    def stop_move(self):
        if self.current_state == self.MOVING_STATE:
            self.current_state = self.IDLE_STATE
            if self.holding:
                self.set_animation(self.HOLD_ANIMATION)
            else:
                self.set_animation(self.IDLE_ANIMATION)

    def start_running(self):
        if self.current_state == self.USING_STATE:
            return
        self.running = True
        if self.current_animation != self.RUN_ANIMATION:
            self.set_animation(self.RUN_ANIMATION)

    def stop_running(self):
        if self.current_state == self.USING_STATE:
            return
        self.running = False
        if self.current_state == self.MOVING_STATE:
            self.set_animation(self.WALK_ANIMATION)

    def update_tile_position(self):
        self.tile_x = self.pos_x // self.TILE_SIZE
        self.reticle_x = self.tile_x
        if self.current_direction == self.LEFT:
            self.reticle_x -= 1
        elif self.current_direction == self.RIGHT:
            self.reticle_x += 1

        self.tile_y = self.pos_y // self.TILE_SIZE
        self.reticle_y = self.tile_y
        if self.current_direction == self.DOWN:
            self.reticle_y += 1
        elif self.current_direction == self.UP:
            self.reticle_y -= 1

    def on_frame(self):
        if self.current_frame == self.TILLING_FRAME:
            self.game.till_tile(self.reticle_x, self.reticle_y)
        elif self.current_frame == self.SOWING_FRAME:
            self.game.sow_tile(self.tile_x, self.tile_y)
        elif self.current_frame == self.WATERING_FRAME:
            self.game.water_tile(self.reticle_x, self.reticle_y)

    def update_held_item_rect(self):
        self.item_screen_rect.topleft = (self.pos_x + self.ITEM_OFFSET[0], self.pos_y + self.ITEM_OFFSET[1])

    def update(self):
        self.update_animation()

    def draw(self):
        self.screen.blit(self.spritesheet, self.screen_rect, self.frame_rect)

        if self.current_state == self.SWITCHING_STATE:
            self.screen.blit(self.tool_sheet, self.tool_screen_rect, self.tool_frame_rect)

        if self.holding:
            self.screen.blit(self.item_sheet, self.item_screen_rect, self.item_frame_rect)