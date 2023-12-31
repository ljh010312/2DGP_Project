import math
import random

from pico2d import load_image, draw_rectangle, clamp, get_time, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_d, SDLK_a, SDLK_w, SDLK_s, SDL_MOUSEBUTTONDOWN, \
    SDL_BUTTON_LEFT, SDL_MOUSEBUTTONUP, SDLK_SPACE, SDLK_1, SDLK_2, SDLK_3

import game_framework
import game_world
import server
import physical
from power_up_item import Power_Up_Item
from shrink_potion import Shrink_Potion
from big_ball_potion import Big_Ball_Potion


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

PIXEL_PER_METER = physical.PIXEL_PER_METER
RUN_SPEED_KMPH = 13.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def time_out(e):
    return e[0] == 'TIME_OUT'


def hit_by_the_ball(e):
    return e[0] == 'HIT'


def out(e):
    return e[0] == 'OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def left_mouse_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT


def left_mouse_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT


class Out:
    @staticmethod
    def enter(keiko, e):
        keiko.wait_time = get_time()

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):
        if get_time() - keiko.wait_time > 1:
            game_world.remove_object(keiko)

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x, keiko.y - 10, 91 / keiko.shrink, 15)
        keiko.image.clip_draw(650, 334, 91, 35, keiko.x, keiko.y, 91 / keiko.shrink, 35 / keiko.shrink)


class Hit_motion:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        keiko.x -= RUN_SPEED_PPS * game_framework.frame_time
        keiko.y -= (RUN_SPEED_PPS / 2) * game_framework.frame_time
        if keiko.frame > 7.5:
            keiko.state_machine.handle_event(('OUT', 0))

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - hit_motion[int(keiko.frame)].h / (2 * keiko.shrink),
                                     hit_motion[int(keiko.frame)].w / keiko.shrink, 15)
        keiko.image.clip_draw(hit_motion[int(keiko.frame)].x, hit_motion[int(keiko.frame)].y,
                              hit_motion[int(keiko.frame)].w,
                              hit_motion[int(keiko.frame)].h, keiko.x, keiko.y,
                              hit_motion[int(keiko.frame)].w / keiko.shrink,
                              hit_motion[int(keiko.frame)].h / keiko.shrink)


class Catch:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        keiko.face_dir = 1
        keiko.wait_time = get_time()
        keiko.catch = True

    @staticmethod
    def exit(keiko, e):
        keiko.catch = False

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - keiko.wait_time > 0.4:
            keiko.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - catch_motion[int(keiko.frame)].h / (2 * keiko.shrink),
                                     catch_motion[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.face_dir == 1:
            keiko.image.clip_draw(catch_motion[int(keiko.frame)].x, catch_motion[int(keiko.frame)].y,
                                  catch_motion[int(keiko.frame)].w,
                                  catch_motion[int(keiko.frame)].h, keiko.x, keiko.y,
                                  catch_motion[int(keiko.frame)].w / keiko.shrink,
                                  catch_motion[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(catch_motion[int(keiko.frame)].x, catch_motion[int(keiko.frame)].y,
                                            catch_motion[int(keiko.frame)].w,
                                            catch_motion[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            catch_motion[int(keiko.frame)].w / keiko.shrink,
                                            catch_motion[int(keiko.frame)].h / keiko.shrink)


class Charging:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        keiko.charging = True
        keiko.face_dir = 1 if keiko.x - e[1].x < 0 else -1

    @staticmethod
    def exit(keiko, e):
        keiko.charging = False
        keiko.power = physical.kmph_to_pps(keiko.power)

    @staticmethod
    def do(keiko):
        keiko.power += 0.2
        keiko.power = clamp(1, keiko.power, keiko.max_power)

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x, keiko.y - throw_motion[0].h / (2 * keiko.shrink),
                                     throw_motion[0].w / keiko.shrink, 15)
        if keiko.face_dir == 1:
            keiko.image.clip_draw(throw_motion[0].x, throw_motion[0].y,
                                  throw_motion[0].w,
                                  throw_motion[0].h, keiko.x, keiko.y, throw_motion[0].w / keiko.shrink,
                                  throw_motion[0].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(throw_motion[0].x, throw_motion[0].y,
                                            throw_motion[0].w,
                                            throw_motion[0].h, 0, 'h', keiko.x, keiko.y,
                                            throw_motion[0].w / keiko.shrink,
                                            throw_motion[0].h / keiko.shrink)


class Throw_Ball:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        keiko.throw_sound.play()
        keiko.hold_ball = False
        keiko.wait_time = get_time()
        keiko.face_dir = 1 if keiko.x - e[1].x < 0 else -1
        if keiko.item == 'ball':
            server.ball.__dict__.update({"x": keiko.x - 20, "y": keiko.y + 25, "z": 40, "z_speed": 0,
                                         "target_x": e[1].x, "target_y": 800 - 1 - e[1].y, "is_bound": False,
                                         "bound_count": 0,
                                         "power": keiko.power, "state": 'KeikoThrow'})
            server.ball.direction = math.atan2(server.ball.target_y - server.ball.y,
                                               server.ball.target_x - server.ball.x)
        elif keiko.item == 'big_ball':
            server.ball.__dict__.update({"x": keiko.x - 20, "y": keiko.y + 25, "z": 40, "z_speed": 0,
                                         "target_x": e[1].x, "target_y": 800 - 1 - e[1].y, "is_bound": False,
                                         "bound_count": 0, "scale": 2, "scale_time": get_time(),
                                         "power": keiko.power, "state": 'KeikoThrow'})
            server.ball.direction = math.atan2(server.ball.target_y - server.ball.y,
                                               server.ball.target_x - server.ball.x)
            keiko.item = 'ball'

    @staticmethod
    def exit(keiko, e):
        keiko.power = 0

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - keiko.wait_time > 0.4:
            keiko.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - throw_motion[int(keiko.frame)].h / (2 * keiko.shrink),
                                     throw_motion[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.face_dir == 1:
            keiko.image.clip_draw(throw_motion[int(keiko.frame)].x, throw_motion[int(keiko.frame)].y,
                                  throw_motion[int(keiko.frame)].w,
                                  throw_motion[int(keiko.frame)].h, keiko.x, keiko.y,
                                  throw_motion[int(keiko.frame)].w / keiko.shrink,
                                  throw_motion[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(throw_motion[int(keiko.frame)].x, throw_motion[int(keiko.frame)].y,
                                            throw_motion[int(keiko.frame)].w,
                                            throw_motion[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            throw_motion[int(keiko.frame)].w / keiko.shrink,
                                            throw_motion[int(keiko.frame)].h / keiko.shrink)


class Up_Down:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        if up_down(e) or down_up(e):
            keiko.v_dir = 1
        elif down_down(e) or up_up(e):
            keiko.v_dir = -1

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        keiko.y += keiko.v_dir * keiko.speed * game_framework.frame_time

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - move_lr[int(keiko.frame)].h / (2 * keiko.shrink),
                                     move_lr[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.face_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h, keiko.x, keiko.y,
                                  move_lr[int(keiko.frame)].w / keiko.shrink,
                                  move_lr[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y,
                                            move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            move_lr[int(keiko.frame)].w / keiko.shrink,
                                            move_lr[int(keiko.frame)].h / keiko.shrink)


class Run:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        if right_down(e) or left_up(e):
            keiko.h_dir, keiko.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            keiko.h_dir, keiko.face_dir = -1, -1

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        keiko.x += keiko.h_dir * keiko.speed * game_framework.frame_time

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - move_lr[int(keiko.frame)].h / (2 * keiko.shrink),
                                     move_lr[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.h_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h, keiko.x, keiko.y,
                                  move_lr[int(keiko.frame)].w / keiko.shrink,
                                  move_lr[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y,
                                            move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            move_lr[int(keiko.frame)].w / keiko.shrink,
                                            move_lr[int(keiko.frame)].h / keiko.shrink)


class Dia_Run:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        if right_down(e) or left_up(e):
            keiko.h_dir, keiko.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            keiko.h_dir, keiko.face_dir = -1, -1

        if up_down(e) or down_up(e):
            keiko.v_dir = 1
        elif down_down(e) or up_up(e):
            keiko.v_dir = -1

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):

        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        keiko.x += keiko.h_dir * keiko.speed * game_framework.frame_time
        keiko.y += keiko.v_dir * keiko.speed * game_framework.frame_time

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - move_lr[int(keiko.frame)].h / (2 * keiko.shrink),
                                     move_lr[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.h_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h, keiko.x, keiko.y,
                                  move_lr[int(keiko.frame)].w / keiko.shrink,
                                  move_lr[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y,
                                            move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            move_lr[int(keiko.frame)].w / keiko.shrink,
                                            move_lr[int(keiko.frame)].h / keiko.shrink)


class Idle:
    @staticmethod
    def enter(keiko, e):
        keiko.h_dir = 0
        keiko.frame = 0

    @staticmethod
    def exit(keiko, e):
        pass

    @staticmethod
    def do(keiko):
        keiko.frame = (keiko.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(keiko):
        keiko.shadow_image.clip_draw(90, 157, 844, 144, keiko.x,
                                     keiko.y - idle_state[int(keiko.frame)].h / (2 * keiko.shrink),
                                     idle_state[int(keiko.frame)].w / keiko.shrink, 15)
        if keiko.face_dir == 1:
            keiko.image.clip_draw(idle_state[int(keiko.frame)].x, idle_state[int(keiko.frame)].y,
                                  idle_state[int(keiko.frame)].w,
                                  idle_state[int(keiko.frame)].h, keiko.x, keiko.y,
                                  idle_state[int(keiko.frame)].w / keiko.shrink,
                                  idle_state[int(keiko.frame)].h / keiko.shrink)
        else:
            keiko.image.clip_composite_draw(idle_state[int(keiko.frame)].x, idle_state[int(keiko.frame)].y,
                                            idle_state[int(keiko.frame)].w,
                                            idle_state[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y,
                                            idle_state[int(keiko.frame)].w / keiko.shrink,
                                            idle_state[int(keiko.frame)].h / keiko.shrink)


class StateMachine:
    def __init__(self, keiko):
        self.keiko = keiko
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down, down_down: Up_Down,
                   up_up: Up_Down, down_up: Up_Down, left_mouse_down: Charging, hit_by_the_ball: Hit_motion,
                   space_down: Catch},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Dia_Run,
                  down_down: Dia_Run, up_up: Dia_Run, down_up: Dia_Run, hit_by_the_ball: Hit_motion},
            Up_Down: {up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle, right_down: Dia_Run,
                      left_down: Dia_Run, right_up: Dia_Run, left_up: Dia_Run, hit_by_the_ball: Hit_motion},
            Dia_Run: {up_up: Run, down_up: Run, right_up: Up_Down, left_up: Up_Down, right_down: Up_Down,
                      left_down: Up_Down, up_down: Run, down_down: Run, hit_by_the_ball: Hit_motion},
            Throw_Ball: {time_out: Idle, right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down,
                         down_down: Up_Down,
                         up_up: Up_Down, down_up: Up_Down, hit_by_the_ball: Hit_motion},
            Charging: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down,
                       down_down: Up_Down,
                       up_up: Up_Down, down_up: Up_Down, left_mouse_up: Throw_Ball, hit_by_the_ball: Hit_motion},
            Hit_motion: {out: Out},
            Out: {},
            Catch: {time_out: Idle, right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down,
                    down_down: Up_Down,
                    up_up: Up_Down, down_up: Up_Down, hit_by_the_ball: Hit_motion}
        }

    def start(self):
        self.cur_state.enter(self.keiko, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.keiko)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.keiko, e)
                self.cur_state = next_state
                self.cur_state.enter(self.keiko, e)
                return True  # 성공적으로 이벤트 변환
        return False  # 이벤트를 소모하지 못했다.

    def draw(self):
        self.cur_state.draw(self.keiko)


def is_have(ob):
    for layer in game_world.objects:
        for o in layer:
            if isinstance(o, ob):
                game_world.remove_object(o)
                return True
    return False


class Keiko:
    def __init__(self, x=100, y=100, speed=0, power=0, catch_percentage=0):
        self.x, self.y = x, y
        self.frame = 0
        self.h_dir = 0
        self.v_dir = 0
        self.face_dir = 1
        self.image = load_image('resource/keiko.png')
        self.shadow_image = load_image('resource/shadow.png')
        self.throw_sound = load_wav('resource/throw_ball.wav')
        self.catch_sound = load_wav('resource/catch_ball.wav')
        self.hit_sound = load_wav('resource/bound_ball.wav')
        self.star_image = load_image('resource/item.png')
        self.hit_sound.set_volume(70)
        self.catch_sound.set_volume(70)
        self.throw_sound.set_volume(50)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.hold_ball = False
        self.charging = False
        self.catch = False
        self.catch_percentage = 50 + catch_percentage
        self.max_power = 70 + power
        self.speed = RUN_SPEED_PPS + physical.kmph_to_pps(speed)
        self.power = 0
        self.shrink = 1
        self.shrink_start_time = 0
        self.item = 'ball'

    def update(self):

        self.state_machine.update()
        self.x = clamp(50, self.x, 480)
        self.y = clamp(125, self.y, 435)
        if self.shrink == 2:
            if get_time() - self.shrink_start_time > 5.0:
                self.shrink = 1
                self.speed = self.temp_speed
        if self.charging:
            server.ball.x = self.x - self.face_dir * 20
            server.ball.y = self.y + 25
        elif self.hold_ball:
            server.ball.x = self.x + self.face_dir * 15
            server.ball.y = self.y

    def handle_event(self, event):
        if event.button == SDL_BUTTON_LEFT:
            if self.hold_ball:
                self.state_machine.handle_event(('INPUT', event))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if not self.hold_ball:
                self.state_machine.handle_event(('INPUT', event))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            if is_have(Power_Up_Item):
                self.power = self.max_power
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            if is_have(Shrink_Potion):
                self.shrink = 2
                self.temp_speed = self.speed
                self.speed = physical.kmph_to_pps(25)
                self.shrink_start_time = get_time()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            if is_have(Big_Ball_Potion):
                self.item = 'big_ball'
        else:
            self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.star_image.clip_draw(784, 304, 86, 83, self.x, self.y + 50, 20, 20)
        self.state_machine.draw()

        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15 / self.shrink, self.y - 40 / self.shrink, self.x + 15 / self.shrink, self.y + 40 / self.shrink

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            if not self.hold_ball and other.is_bound and not other.state == 'Hold':
                other.x = self.x + self.h_dir * 15
                other.y = self.y
                other.state = 'Hold'
                other.bound_count = 4
                self.hold_ball = True
            if other.state == 'Throw' and not other.is_bound:
                # 여기에 맞았을 때 추가
                if self.catch:
                    if random.randint(1, 100) < self.catch_percentage:
                        self.catch_sound.play()
                        other.x = self.x + 15
                        other.y = self.y
                        other.z = 0
                        other.power = 0
                        other.bound_count = 4
                        other.state = 'Stay'
                    else:
                        self.hit_sound.play()
                        self.state_machine.handle_event(('HIT', 0))
                        other.direction += math.pi
                else:
                    self.hit_sound.play()
                    self.state_machine.handle_event(('HIT', 0))
                    other.direction += math.pi
