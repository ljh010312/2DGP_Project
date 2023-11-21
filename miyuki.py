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
        return self.x - 20, self.y - 40, self.x + 20, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


    def draw(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


