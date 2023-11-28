from pico2d import *

import random
import math
import game_framework
import game_world
import server
from ball import Ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
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
    Frame(219, 1950, 54, 77),
    Frame(219, 1950, 54, 77),
    Frame(284, 1950, 48, 82),
    Frame(284, 1950, 48, 82),
    Frame(342, 1950, 56, 75),
    Frame(342, 1950, 56, 75),
    Frame(409, 1950, 53, 74),
    Frame(409, 1950, 53, 74),
)

hit_motion = (
    Frame(261, 376, 56, 82),
    Frame(261, 376, 56, 82),
    Frame(364, 381, 75, 71),
    Frame(364, 381, 75, 71),
    Frame(443, 381, 82, 67),
    Frame(443, 381, 82, 67),
    Frame(542, 381, 85, 48),
    Frame(643, 381, 98, 45)
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
        self.state = 'Walk'
        self.face_dir = 0
        self.build_behavior_tree()
        self.hold_ball = False
        self.ball = None
        self.power = 0

    def get_bb(self):
        return self.x - 15, self.y - 40, self.x + 15, self.y + 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()
        # self.face_dir = -1 if math.cos(self.dir) < 0 else 1

    def draw(self):
        if self.state == 'Walk':
            if math.cos(self.dir) < 0 or self.face_dir == -1:
                self.image.clip_composite_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                                  move_lr[int(self.frame)].w,
                                  move_lr[int(self.frame)].h, 0, 'h', self.x, self.y, move_lr[int(self.frame)].w,
                                  move_lr[int(self.frame)].h)
            else:
                self.image.clip_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                                               move_lr[int(self.frame)].w,
                                               move_lr[int(self.frame)].h, self.x, self.y, move_lr[int(self.frame)].w,
                                               move_lr[int(self.frame)].h)
        elif self.state == 'Charge':
            self.image.clip_composite_draw(throw_motion[0].x, throw_motion[0].y,
                                           throw_motion[0].w,
                                           throw_motion[0].h, 0, 'h', self.x, self.y,
                                           throw_motion[0].w,
                                           throw_motion[0].h)
        elif self.state == 'Throw':
            self.image.clip_composite_draw(throw_motion[int(self.frame)].x, throw_motion[int(self.frame)].y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h, 0, 'h', self.x, self.y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h)
        elif self.state == 'HitMotion' or self.state == 'Hit':
            self.image.clip_composite_draw(hit_motion[int(self.frame)].x, hit_motion[int(self.frame)].y,
                                           hit_motion[int(self.frame)].w,
                                           hit_motion[int(self.frame)].h, 0, 'h', self.x, self.y,
                                           hit_motion[int(self.frame)].w,
                                           hit_motion[int(self.frame)].h)
        elif self.state == 'OutCount' or self.state == 'Out':
            self.image.clip_composite_draw(hit_motion[7].x, hit_motion[7].y,
                                           hit_motion[7].w,
                                           hit_motion[7].h, 0, 'h', self.x, self.y,
                                           hit_motion[7].w,
                                           hit_motion[7].h)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'miyuki:ball':
            if other.state == 'Stay' and not self.hold_ball:
                self.hold_ball = True
                other.state = 'Hold'
                other.x = self.x + self.face_dir * 15
                other.y = self.y
            elif other.state == 'KeikoThrow':
                self.state = 'Hit'
                other.direction += math.pi



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

    def is_oppenent_hold_ball(self):    # 상대가 공을 잡고 있는지
        if play_mode.keiko.hold_ball:
            self.face_dir = -1
            return BehaviorTree.SUCCESS
        else:
            self.face_dir = 0
            return BehaviorTree.FAIL

    def set_flee_random_location(self): # 코트의 바깥쪽 좌표 구하기
        self.tx, self.ty = random.randint(800, 870), random.randint(127, 435)
        return BehaviorTree.SUCCESS


    def is_court_in_ball(self): # 자신의 코트에 공이 있는 지
        if server.ball.state == 'Stay' and 510 < server.ball.x < 870 and 127 < server.ball.y < 435:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def set_ball_location(self):
        if 510 < server.ball.x < 870 and 127 < server.ball.y < 435:
            self.tx, self.ty = server.ball.x, server.ball.y
        return BehaviorTree.SUCCESS

    def is_hold_ball(self):
        if self.hold_ball:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def charge_power(self):
        self.state = 'Charge'
        server.ball.x = self.x + 20
        server.ball.y = self.y + 30
        if self.power > 3.0:
            return BehaviorTree.SUCCESS
        else:
            self.power += 0.01
            return BehaviorTree.RUNNING

    def throw_ball(self):
        if self.state != 'Throw':
            self.frame = 0
            self.state = 'Throw'
            server.ball.x = self.x + 20
            server.ball.y = self.y + 25
            server.ball.z = 40
            server.ball.target_x = play_mode.keiko.x
            server.ball.target_y = play_mode.keiko.y
            server.ball.power = self.power * 5
            server.ball.direction = math.atan2(server.ball.target_y - server.ball.y, server.ball.target_x - server.ball.x)
            server.ball.state = 'Throw'
            self.power = 0
        if self.frame < 7:
            return BehaviorTree.RUNNING
        else:
            self.hold_ball = False
            return BehaviorTree.SUCCESS

    def is_hit(self):
        if self.state == 'Hit':
            self.frame = 0
            return BehaviorTree.SUCCESS
        elif self.state == 'HitMotion':
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def hit_motion(self):
        if self.state == 'Hit':
            self.state = 'HitMotion'
        if self.frame < 7.9:
            self.x += RUN_SPEED_PPS  * game_framework.frame_time
            self.y -= (RUN_SPEED_PPS / 2) * game_framework.frame_time
            return BehaviorTree.RUNNING
        else:
            self.state = 'Out'
            return BehaviorTree.SUCCESS

    def is_out(self):
        if self.state == 'Out':
            return BehaviorTree.SUCCESS
        elif self.state == 'OutCount':
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def out_count(self):
        if self.state == 'Out':
            self.state = 'OutCount'
            self.wait_time = get_time()

        if get_time() - self.wait_time < 3.0:
            return BehaviorTree.RUNNING
        else:
            game_world.remove_object(self)

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        SEQ_wander = Sequence('Wander', a1, a2)

        c1 = Condition('상대가 공을 잡고 있는지', self.is_oppenent_hold_ball)
        a3 = Action('도망갈 위치 랜덤 설정', self.set_flee_random_location)

        SEQ_flee = Sequence('도망', c1, a3, a2)

        c2 = Condition('코트 공이 있는지', self.is_court_in_ball)
        a4 = Action('공 위치로 설정', self.set_ball_location)

        root = SEQ_ball_loc_move = Sequence('move to ball', c2, a4, a2)

        c3 = Condition('공을 잡고 있는지', self.is_hold_ball)
        a5 = Action('기 모으기', self.charge_power)
        a6 = Action('던지기', self.throw_ball)

        root = SEQ_throw_ball = Sequence('공 던지기', c3, a5, a6)

        SEL_move_to_ball_or_throw_or_wander = Selector('공으로 이동 or 던지기 or 배회', SEQ_ball_loc_move, SEQ_throw_ball, SEQ_wander)
        root = SEL_flee_or_throw =Selector('도망 혹은 공 찾아서 던지기', SEQ_flee, SEL_move_to_ball_or_throw_or_wander)

        c4 = Condition('공과 충돌 했는지', self.is_hit)
        a7 = Action('공 맞는 모션', self.hit_motion)
        root = SEQ_hit_ball = Sequence('공 맞음', c4, a7)

        c5 = Condition('공을 맞아서 누워있는지', self.is_out)
        a8 = Action('아웃 카운트', self.out_count)
        root = SEQ_out = Sequence('아웃카운트 후 미유키 삭제', c5, a8)

        root = SEL_hit_and_out = Selector('out or hit', SEQ_out, SEQ_hit_ball)

        root = SEL_hit_or_move = Selector('hit or move', SEL_hit_and_out, SEL_flee_or_throw)

        self.bt = BehaviorTree(root)