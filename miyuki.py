from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Frame:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


idle_state = (
    Frame(18, 2310, 36, 82),
    Frame(18, 2310, 36, 82),
    Frame(18, 2310, 36, 82),
    Frame(18, 2310, 36, 82),
    Frame(63, 2310, 38, 79),
    Frame(63, 2310, 38, 79),
    Frame(63, 2310, 38, 79),
    Frame(63, 2310, 38, 79),
)

move_lr = (
    Frame(18,2178,36,81),
    Frame(18,2178,36,81),
    Frame(60,2178,41,80),
    Frame(60,2178,41,80),
    Frame(107,2178,36,81),
    Frame(107,2178,36,81),
    Frame(149,2178,41,80),
    Frame(149,2178,41,80),
)


throw_motion = (
    Frame(219, 2418, 54, 77),
    Frame(219, 2418, 54, 77),
    Frame(284, 2418, 48, 82),
    Frame(284, 2418, 48, 82),
    Frame(342, 2418, 56, 75),
    Frame(342, 2418, 56, 75),
    Frame(409, 2418, 53, 74),
    Frame(409, 2418, 53, 74),
)

class Miyuki:
    image = None

    def load_image(self):
        if Miyuki.image == None:
            Miyuki.image = load_image('miyuki.png')

    def __init__(self, x = None, y = None):
        self.x = x if x else random.randint(400, 700)
        self.y = y if y else random.randint(105, 330)
        self.load_image()
        self.dir = 0.0
        self.frame = 0
        self.state = 'Idle'

    def get_bb(self):
        return self.x - 15, self.y - 40, self.x + 15, self.y + 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


    def draw(self):
        self.image.clip_draw(idle_state[int(self.frame)].x, idle_state[int(self.frame)].y,
                              idle_state[int(self.frame)].w,
                              idle_state[int(self.frame)].h, self.x, self.y, idle_state[int(self.frame)].w,
                              idle_state[int(self.frame)].h)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


