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
        self.speed = 0.0
        self.tx, self.ty = 400, 150
        self.frame = 0
        self.state = 'Idle'
        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 15, self.y - 40, self.x + 15, self.y + 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            self.image.clip_composite_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                              move_lr[int(self.frame)].w,
                              move_lr[int(self.frame)].h, 0, 'h', self.x, self.y, move_lr[int(self.frame)].w,
                              move_lr[int(self.frame)].h)
        else:
            self.image.clip_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                                           move_lr[int(self.frame)].w,
                                           move_lr[int(self.frame)].h, self.x, self.y, move_lr[int(self.frame)].w,
                                           move_lr[int(self.frame)].h)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2


    def build_behavior_tree(self):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r = 0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(510, 870), random.randint(127, 435)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)

        self.bt = BehaviorTree(root)