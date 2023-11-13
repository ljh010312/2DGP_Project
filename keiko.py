# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, draw_rectangle, clamp, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_d, SDLK_a, SDLK_w, SDLK_s, SDL_MOUSEBUTTONDOWN, \
    SDL_BUTTON_LEFT, SDL_MOUSEBUTTONUP

import game_framework
import game_world
from ball import Ball, Big_Ball


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

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


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


class Charging:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        keiko.charging = True

    @staticmethod
    def exit(keiko, e):
        keiko.charging = False

    @staticmethod
    def do(keiko):
        keiko.power += 0.01
        keiko.power = clamp(1, keiko.power, 10)

    @staticmethod
    def draw(keiko):
        keiko.image.clip_draw(throw_motion[0].x, throw_motion[0].y,
                              throw_motion[0].w,
                              throw_motion[0].h, keiko.x, keiko.y, throw_motion[0].w / keiko.shrink,
                              throw_motion[0].h / keiko.shrink)


class Throw_Ball:
    @staticmethod
    def enter(keiko, e):
        keiko.frame = 0
        keiko.hold_ball = False
        keiko.wait_time = get_time()
        game_world.remove_object(keiko.ball)

        if keiko.item == 'ball':
            ball = Ball(keiko.x-20, keiko.y+25, e[1].x, 600 - 1 - e[1].y, keiko.power * 5)
            game_world.add_object(ball)
        elif keiko.item == 'big_ball':
            big_ball = Big_Ball(keiko.x-20, keiko.y+25, e[1].x, 600 - 1 - e[1].y, keiko.power * 5)
            game_world.add_object(big_ball)
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
        keiko.image.clip_draw(throw_motion[int(keiko.frame)].x, throw_motion[int(keiko.frame)].y,
                              throw_motion[int(keiko.frame)].w,
                              throw_motion[int(keiko.frame)].h, keiko.x, keiko.y,
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
        keiko.y += keiko.v_dir * RUN_SPEED_PPS * game_framework.frame_time
        keiko.y = clamp(105, keiko.y, 330)

    @staticmethod
    def draw(keiko):
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

        keiko.x += keiko.h_dir * RUN_SPEED_PPS * game_framework.frame_time
        keiko.x = clamp(90, keiko.x, 375)

    @staticmethod
    def draw(keiko):
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

        keiko.x += keiko.h_dir * RUN_SPEED_PPS * game_framework.frame_time
        keiko.y += keiko.v_dir * RUN_SPEED_PPS * game_framework.frame_time

        keiko.x = clamp(90, keiko.x, 375)
        keiko.y = clamp(105, keiko.y, 330)

    @staticmethod
    def draw(keiko):
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
                   up_up: Up_Down, down_up: Up_Down, left_mouse_down: Charging},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Dia_Run,
                  down_down: Dia_Run, up_up: Dia_Run, down_up: Dia_Run},
            Up_Down: {up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle, right_down: Dia_Run,
                      left_down: Dia_Run, right_up: Dia_Run, left_up: Dia_Run},
            Dia_Run: {up_up: Run, down_up: Run, right_up: Up_Down, left_up: Up_Down, right_down: Up_Down,
                      left_down: Up_Down, up_down: Run, down_down: Run},
            Throw_Ball: {time_out: Idle, right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down,
                         down_down: Up_Down,
                         up_up: Up_Down, down_up: Up_Down},
            Charging: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down,
                       down_down: Up_Down,
                       up_up: Up_Down, down_up: Up_Down, left_mouse_up: Throw_Ball}
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


class Keiko:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.h_dir = 0
        self.v_dir = 0
        self.face_dir = 1
        self.image = load_image('keiko.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.hold_ball = False
        self.charging = False
        self.ball = None
        self.power = 0
        self.shrink = 1
        self.shrink_start_time = 0
        self.item = 'ball'

    def update(self):
        self.state_machine.update()
        if self.shrink == 2:
            if get_time() - self.shrink_start_time > 5.0:
                self.shrink = 1
        if self.charging:
            self.ball.x = self.x - 20
            self.ball.y = self.y + 25
        elif self.hold_ball:
            self.ball.x = self.x + self.face_dir * 15
            self.ball.y = self.y

    def handle_event(self, event):
        if event.button == SDL_BUTTON_LEFT:
            if self.hold_ball:
                self.state_machine.handle_event(('INPUT', event))
        else:
            self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15 / self.shrink, self.y - 40 / self.shrink, self.x + 15 / self.shrink, self.y + 40 / self.shrink

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            if not self.hold_ball:
                self.ball = Ball(self.x + self.h_dir * 15, self.y, self.x, self.y, 0)
                self.hold_ball = True
                game_world.add_object(self.ball)
                game_world.remove_object(other)
        elif group == 'keiko:power_up_item':
            self.power = 10
            game_world.remove_object(other)
        elif group == 'keiko:shrink_potion':
            self.shrink = 2
            self.shrink_start_time = get_time()
            game_world.remove_object(other)
        elif group == 'keiko:big_ball_potion':
            self.item = 'big_ball'
            game_world.remove_object(other)
