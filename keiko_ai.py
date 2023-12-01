from pico2d import *

import random
import math
import game_framework
import game_world
import physical
import server
from ball import Ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode

PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 40 cm
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
    Frame(24, 2122, 33, 75),
    Frame(24, 2122, 33, 75),
    Frame(24, 2122, 33, 75),
    Frame(24, 2122, 33, 75),
    Frame(24, 2122, 33, 73),
    Frame(24, 2122, 33, 73),
    Frame(24, 2122, 33, 73),
    Frame(24, 2122, 33, 73),
)

move_lr = (
    Frame(24, 2027, 40, 75),
    Frame(24, 2027, 40, 75),
    Frame(81, 2027, 40, 75),
    Frame(81, 2027, 40, 75),
    Frame(139, 2027, 37, 77),
    Frame(139, 2027, 37, 77),
    Frame(190, 2027, 42, 76),
    Frame(190, 2027, 42, 76)
)

throw_motion = (
    Frame(492, 1814, 54, 76),
    Frame(492, 1814, 54, 76),
    Frame(570, 1814, 41, 75),
    Frame(570, 1814, 41, 75),
    Frame(637, 1814, 61, 68),
    Frame(637, 1814, 61, 68),
    Frame(712, 1814, 66, 67),
    Frame(712, 1814, 66, 67),
)

hit_motion = (
    Frame(257, 315, 43, 68),
    Frame(257, 315, 43, 68),
    Frame(363, 320, 60, 63),
    Frame(363, 320, 60, 63),
    Frame(448, 323, 69, 57),
    Frame(448, 323, 69, 57),
    Frame(544, 331, 87, 36),
    Frame(544, 331, 87, 36)
)

catch_motion = (
    Frame(15, 1814, 36, 73),
    Frame(15, 1814, 36, 73),
    Frame(64, 1814, 52, 72),
    Frame(64, 1814, 52, 72),
    Frame(127, 1814, 41, 69),
    Frame(127, 1814, 41, 69),
    Frame(127, 1814, 41, 69),
    Frame(127, 1814, 41, 69),
)

class Keiko_AI:
    image = None
    shadow_image = None

    def load_image(self):
        if Keiko_AI.image == None:
            Keiko_AI.image = load_image('resource/keiko.png')
            Keiko_AI.shadow_image = load_image('resource/shadow.png')

    def __init__(self, x=None, y=None, catch_percentage= 100):
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
        self.catch_percentage = catch_percentage

    def get_bb(self):
        return self.x - 15, self.y - 40, self.x + 15, self.y + 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()
        # self.face_dir = -1 if math.cos(self.dir) < 0 else 1

    def draw(self):
        if self.state == 'Walk':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - move_lr[int(self.frame)].h / 2,
                                         move_lr[int(self.frame)].w, 15)
            if math.cos(self.dir) < 0 or self.face_dir == -1:
                self.image.clip_composite_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                                               move_lr[int(self.frame)].w,
                                               move_lr[int(self.frame)].h, 0, 'h', self.x, self.y,
                                               move_lr[int(self.frame)].w,
                                               move_lr[int(self.frame)].h)
            else:
                self.image.clip_draw(move_lr[int(self.frame)].x, move_lr[int(self.frame)].y,
                                     move_lr[int(self.frame)].w,
                                     move_lr[int(self.frame)].h, self.x, self.y, move_lr[int(self.frame)].w,
                                     move_lr[int(self.frame)].h)
        elif self.state == 'Charge':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - throw_motion[0].h / 2,
                                        throw_motion[0].w, 15)
            self.image.clip_draw(throw_motion[0].x, throw_motion[0].y,
                                           throw_motion[0].w,
                                           throw_motion[0].h, self.x, self.y,
                                           throw_motion[0].w,
                                           throw_motion[0].h)
        elif self.state == 'Throw':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - throw_motion[int(self.frame)].h / 2,
                                        throw_motion[int(self.frame)].w, 15)
            self.image.clip_draw(throw_motion[int(self.frame)].x, throw_motion[int(self.frame)].y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h,  self.x, self.y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h)
        elif self.state == 'HitMotion' or self.state == 'Hit':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - hit_motion[int(self.frame)].h / 2,
                                         hit_motion[int(self.frame)].w, 15)
            self.image.clip_draw(hit_motion[int(self.frame)].x, hit_motion[int(self.frame)].y,
                                  hit_motion[int(self.frame)].w,
                                  hit_motion[int(self.frame)].h, self.x, self.y,
                                  hit_motion[int(self.frame)].w,
                                  hit_motion[int(self.frame)].h )
        elif self.state == 'OutCount' or self.state == 'Out':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - 10, 91 , 15)
            self.image.clip_draw(650, 334, 91, 35, self.x, self.y, 91 , 35 )
        elif self.state == 'CatchMotion' or self.state == 'Catch':
            pass
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - catch_motion[int(self.frame)].h / 2,
                                        catch_motion[int(self.frame)].w, 15)
            self.image.clip_draw(catch_motion[int(self.frame)].x, catch_motion[int(self.frame)].y,
                                           catch_motion[int(self.frame)].w,
                                           catch_motion[int(self.frame)].h, self.x, self.y,
                                           catch_motion[int(self.frame)].w,
                                           catch_motion[int(self.frame)].h)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if self.state == 'Out' or self.state == 'OutCount':
            return
        if group == 'keiko:ball':
            if other.is_bound and not self.hold_ball and not other.state == 'Hold':
                self.hold_ball = True
                other.state = 'Hold'
                other.x = self.x + self.face_dir * 15
                other.y = self.y
            elif other.state == 'Throw' and not other.is_bound:
                if self.can_catch():
                    self.state = 'Catch'
                    self.hold_ball = True
                    other.state = 'Hold'
                    other.x = self.x + self.face_dir * 15
                    other.y = self.y
                else:
                    self.state = 'Hit'
                    other.direction += math.pi

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2


    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time


    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 490), random.randint(127, 435)
        return BehaviorTree.SUCCESS

    def is_oppenent_hold_ball(self):  # 상대가 공을 잡고 있는지
        for miyuki in play_mode.miyuki_ai:
            if miyuki.hold_ball:
                self.face_dir = -1
                return BehaviorTree.SUCCESS
        self.face_dir = 0
        return BehaviorTree.FAIL

    def set_flee_random_location(self):  # 코트의 바깥쪽 좌표 구하기
        self.tx, self.ty = random.randint(100, 170), random.randint(127, 435)
        return BehaviorTree.SUCCESS

    def is_court_in_ball(self):  # 자신의 코트에 공이 있는 지
        if server.ball.state == 'Stay' and 50 < server.ball.x < 490 and 127 < server.ball.y < 435:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_ball_location(self):
        if 50 < server.ball.x < 490 and 127 < server.ball.y < 435:
            self.tx, self.ty = server.ball.x, server.ball.y
        return BehaviorTree.SUCCESS

    def is_hold_ball(self):
        if self.hold_ball:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def charge_power(self):
        self.state = 'Charge'
        server.ball.x = self.x - 20
        server.ball.y = self.y + 30
        if self.power > 60.0:
            self.power = physical.kmph_to_pps(self.power)
            return BehaviorTree.SUCCESS
        else:
            self.power += 0.2
            return BehaviorTree.RUNNING

    def throw_ball(self):
        if self.state != 'Throw':
            server.ball.__dict__.update({"x": self.x + 20, "y": self.y + 25, "z": 40, "z_speed": 0,
                                         "target_x": play_mode.keiko.x, "target_y": play_mode.keiko.y,
                                         "is_bound": False,
                                         "power": self.power, "state": 'KeikoThrow'})
            server.ball.direction = math.atan2(server.ball.target_y - server.ball.y,
                                               server.ball.target_x - server.ball.x)
            self.frame = 0
            self.state = 'Throw'
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
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
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

    def is_miyuki_throw_ball(self):
        if server.ball.state == 'Throw' and not server.ball.is_bound:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def flee_from_ball(self):
        self.state = 'Walk'
        self.dir = math.atan2(self.y - server.ball.y, self.x - server.ball.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.face_dir = 1
        return BehaviorTree.RUNNING

    def can_catch(self):
        random_num = random.randint(1, 100)
        if random_num < self.catch_percentage:
            return True
        else:
            return False

    def is_catch(self):
        if self.state == 'Catch':
            self.frame = 0
            return BehaviorTree.SUCCESS
        elif self.state == 'CatchMotion':
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def catch_motion(self):
        if self.state == 'Catch':
            self.state = 'CatchMotion'
        if self.frame < 7.9:
            self.x -= server.ball.power / 10 * game_framework.frame_time
            server.ball.x = self.x + 15
            server.ball.y = self.y
            return BehaviorTree.RUNNING
        else:
            self.state = 'Walk'
            return BehaviorTree.SUCCESS


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

        c6 = Condition('상대가 공을 던졌는지', self.is_miyuki_throw_ball)
        a9 = Action('공의 반대쪽으로 이동', self.flee_from_ball)

        root = SEQ_flee_from_ball = Sequence('flee from ball', c6, a9)

        c3 = Condition('공을 잡고 있는지', self.is_hold_ball)
        a5 = Action('기 모으기', self.charge_power)
        a6 = Action('던지기', self.throw_ball)

        root = SEQ_throw_ball = Sequence('공 던지기', c3, a5, a6)

        SEL_move_to_ball_or_throw_or_wander = Selector('공으로 이동 or 던지기 or 배회', SEQ_flee_from_ball,SEQ_ball_loc_move, SEQ_throw_ball,
                                                       SEQ_wander)
        root = SEL_flee_or_throw = Selector('도망 혹은 공 찾아서 던지기', SEQ_flee, SEL_move_to_ball_or_throw_or_wander)

        c4 = Condition('공과 충돌 했는지', self.is_hit)
        a7 = Action('공 맞는 모션', self.hit_motion)
        root = SEQ_hit_ball = Sequence('공 맞음', c4, a7)

        c5 = Condition('공을 맞아서 누워있는지', self.is_out)
        a8 = Action('아웃 카운트', self.out_count)
        root = SEQ_out = Sequence('아웃카운트 후 미유키 삭제', c5, a8)

        c7 = Condition("공을 잡았는지", self.is_catch)
        a10 = Action("공 잡는 모션", self.catch_motion)
        root = SEQ_catch = Sequence('Catch ball', c7, a10)

        root = SEL_hit_or_out = Selector('catch or out or hit', SEQ_catch, SEQ_out, SEQ_hit_ball)

        root = SEL_hit_or_move = Selector('hit or move', SEL_hit_or_out, SEL_flee_or_throw)


        self.bt = BehaviorTree(root)
