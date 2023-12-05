from pico2d import *

import random
import math
import game_framework
import game_world
import keiko
import keiko_ai
import physical
import server
from ball import Ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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
    Frame(18, 2178, 36, 81),
    Frame(18, 2178, 36, 81),
    Frame(60, 2178, 41, 80),
    Frame(60, 2178, 41, 80),
    Frame(107, 2178, 36, 81),
    Frame(107, 2178, 36, 81),
    Frame(149, 2178, 41, 80),
    Frame(149, 2178, 41, 80),
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

catch_motion = (
    Frame(18, 1950, 43, 81),
    Frame(18, 1950, 43, 81),
    Frame(70, 1950, 55, 79),
    Frame(70, 1950, 55, 79),
    Frame(134, 1950, 43, 83),
    Frame(134, 1950, 43, 83),
    Frame(134, 1950, 43, 83),
    Frame(134, 1950, 43, 83)
)


class Miyuki:
    image = None
    image_one = None
    image_two = None
    image_three = None
    shadow_image = None
    catch_sound = None
    throw_sound = None
    hit_sound = None

    def load_image(self):
        if Miyuki.image == None:
            Miyuki.image = load_image('resource/miyuki.png')
            Miyuki.image_one = load_image('resource/miyuki.png')
            Miyuki.image_two = load_image('resource/miyuki2.png')
            Miyuki.image_three = load_image('resource/miyuki3.png')
            Miyuki.shadow_image = load_image('resource/shadow.png')
            Miyuki.catch_sound = load_wav('resource/catch_ball.wav')
            Miyuki.hit_sound = load_wav('resource/bound_ball.wav')
            Miyuki.throw_sound = load_wav('resource/throw_ball.wav')
            Miyuki.throw_sound.set_volume(50)
            Miyuki.hit_sound.set_volume(70)
            Miyuki.catch_sound.set_volume(70)

    def __init__(self, x=None, y=None, speed=0, max_power=0, catch_percentage=60, select_image=1):
        self.x = x if x else random.randint(400, 700)
        self.y = y if y else random.randint(105, 330)
        self.load_image()
        self.dir = 0.0
        self.speed = speed
        self.tx, self.ty = 400, 150
        self.frame = 0
        self.state = 'Walk'
        self.face_dir = 0
        self.build_behavior_tree()
        self.hold_ball = False
        self.ball = None
        self.power = 0
        self.max_power = max_power
        self.catch_percentage = catch_percentage
        self.select_image = select_image

    def get_bb(self):
        return self.x - 15, self.y - 40, self.x + 15, self.y + 40

    def update(self):
        self.image_update()
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
            self.image.clip_composite_draw(throw_motion[0].x, throw_motion[0].y,
                                           throw_motion[0].w,
                                           throw_motion[0].h, 0, 'h', self.x, self.y,
                                           throw_motion[0].w,
                                           throw_motion[0].h)
        elif self.state == 'Throw':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - throw_motion[int(self.frame)].h / 2,
                                        throw_motion[int(self.frame)].w, 15)
            self.image.clip_composite_draw(throw_motion[int(self.frame)].x, throw_motion[int(self.frame)].y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h, 0, 'h', self.x, self.y,
                                           throw_motion[int(self.frame)].w,
                                           throw_motion[int(self.frame)].h)
        elif self.state == 'HitMotion' or self.state == 'Hit':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - 15,
                                        hit_motion[int(self.frame)].w, 15)
            self.image.clip_composite_draw(hit_motion[int(self.frame)].x, hit_motion[int(self.frame)].y,
                                           hit_motion[int(self.frame)].w,
                                           hit_motion[int(self.frame)].h, 0, 'h', self.x, self.y,
                                           hit_motion[int(self.frame)].w,
                                           hit_motion[int(self.frame)].h)
        elif self.state == 'OutCount' or self.state == 'Out':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - 15,
                                        hit_motion[7].w, 15)
            self.image.clip_composite_draw(hit_motion[7].x, hit_motion[7].y,
                                           hit_motion[7].w,
                                           hit_motion[7].h, 0, 'h', self.x, self.y,
                                           hit_motion[7].w,
                                           hit_motion[7].h)
        elif self.state == 'CatchMotion' or self.state == 'Catch':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.y - catch_motion[int(self.frame)].h / 2,
                                        catch_motion[int(self.frame)].w, 15)
            self.image.clip_composite_draw(catch_motion[int(self.frame)].x, catch_motion[int(self.frame)].y,
                                           catch_motion[int(self.frame)].w,
                                           catch_motion[int(self.frame)].h, 0, 'h', self.x, self.y,
                                           catch_motion[int(self.frame)].w,
                                           catch_motion[int(self.frame)].h)

    def image_update(self):
        if self.select_image == 1:
            self.image = self.image_one
        elif self.select_image == 2:
            self.image = self.image_two
        else:
            self.image = self.image_three

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if self.state == 'Out' or self.state == 'OutCount':
            return
        if group == 'miyuki:ball':
            if other.is_bound and not self.hold_ball and not other.state == 'Hold':
                self.hold_ball = True
                other.state = 'Hold'
                other.x = self.x + self.face_dir * 15
                other.y = self.y
                other.bound_count = 4
            elif other.state == 'KeikoThrow' and not other.is_bound:
                if self.can_catch():
                    self.catch_sound.play()
                    self.state = 'Catch'
                    self.hold_ball = True
                    other.state = 'Hold'
                    other.x = self.x + self.face_dir * 15
                    other.y = self.y
                    other.bound_count = 4
                else:
                    self.hit_sound.play()
                    self.state = 'Hit'
                    other.direction += math.pi

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=2):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(510, 870), random.randint(127, 435)
        return BehaviorTree.SUCCESS

    def is_oppenent_hold_ball(self):  # 상대가 공을 잡고 있는지
        for layer in game_world.objects:
            for o in layer:
                if isinstance(o, keiko.Keiko) or isinstance(o, keiko_ai.Keiko_AI):
                    if o.hold_ball:
                        self.face_dir = -1
                        return BehaviorTree.SUCCESS
        self.face_dir = 0
        return BehaviorTree.FAIL

    def set_flee_random_location(self):  # 코트의 바깥쪽 좌표 구하기
        self.tx, self.ty = random.randint(650, 700), random.randint(127, 435)
        return BehaviorTree.SUCCESS

    def is_court_in_ball(self):  # 자신의 코트에 공이 있는 지
        if server.ball.state == 'Stay' and 485 < server.ball.x < 950 and 120 < server.ball.y < 440:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_ball_location(self):
        if 485 < server.ball.x < 950 and 120 < server.ball.y < 440:
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
        if self.power > self.max_power:
            self.power = physical.kmph_to_pps(self.power)
            return BehaviorTree.SUCCESS
        else:
            self.power += 0.2
            return BehaviorTree.RUNNING

    def throw_ball(self):
        tx, ty = 450, 200
        for layer in game_world.objects:
            for o in layer:
                if isinstance(o, keiko_ai.Keiko_AI) or isinstance(o, keiko.Keiko):
                    tx, ty = o.x, o.y
                    break
        if self.state != 'Throw':
            server.ball.__dict__.update({"x": self.x + 20, "y": self.y + 25, "z": 40, "z_speed": 0,
                                         "target_x": tx, "target_y": ty,
                                         "is_bound": False, "bound_count": 0,
                                         "power": self.power, "state": 'Throw'})
            server.ball.direction = math.atan2(server.ball.target_y - server.ball.y,
                                               server.ball.target_x - server.ball.x)
            self.frame = 0
            self.state = 'Throw'
            self.power = 0
            self.throw_sound.play()
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
            self.x += RUN_SPEED_PPS * game_framework.frame_time
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

    def is_keiko_throw_ball(self):
        if server.ball.state == 'KeikoThrow' and not server.ball.is_bound:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def flee_from_ball(self):
        self.state = 'Walk'
        self.dir = math.atan2(self.y - server.ball.y, self.x - server.ball.x)
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(480, self.x, 950)
        self.y = clamp(125, self.y, 435)
        self.face_dir = -1
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
            self.x += server.ball.power / 10 * game_framework.frame_time
            server.ball.x = self.x - 15
            server.ball.y = self.y
            self.opp_not_hold()
            return BehaviorTree.RUNNING
        else:
            self.state = 'Walk'
            self.opp_not_hold()
            return BehaviorTree.SUCCESS

    def opp_not_hold(self):
        for layer in game_world.objects:
            for o in layer:
                if isinstance(o, keiko_ai.Keiko_AI) or isinstance(o, keiko.Keiko):
                    o.hold_ball = False

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

        c6 = Condition('상대가 공을 던졌는지', self.is_keiko_throw_ball)
        a9 = Action('공의 반대쪽으로 이동', self.flee_from_ball)

        root = SEQ_flee_from_ball = Sequence('flee from ball', c6, a9)

        c3 = Condition('공을 잡고 있는지', self.is_hold_ball)
        a5 = Action('기 모으기', self.charge_power)
        a6 = Action('던지기', self.throw_ball)

        root = SEQ_throw_ball = Sequence('공 던지기', c3, a5, a6)

        SEL_move_to_ball_or_throw_or_wander = Selector('공으로 이동 or 던지기 or 배회', SEQ_flee_from_ball, SEQ_ball_loc_move,
                                                       SEQ_throw_ball,
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
