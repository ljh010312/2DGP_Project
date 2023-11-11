# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_d, SDLK_a, SDLK_w, SDLK_s

import game_framework


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

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


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


    @staticmethod
    def draw(keiko):
        if keiko.face_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                   move_lr[int(keiko.frame)].h, keiko.x, keiko.y,  move_lr[int(keiko.frame)].w,
                                   move_lr[int(keiko.frame)].h)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                   move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y, move_lr[int(keiko.frame)].w,
                                   move_lr[int(keiko.frame)].h)



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

    @staticmethod
    def draw(keiko):
        if keiko.h_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h, keiko.x, keiko.y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y, move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h)


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

    @staticmethod
    def draw(keiko):
        if keiko.h_dir > 0:
            keiko.image.clip_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h, keiko.x, keiko.y, move_lr[int(keiko.frame)].w,
                                  move_lr[int(keiko.frame)].h)
        else:
            keiko.image.clip_composite_draw(move_lr[int(keiko.frame)].x, move_lr[int(keiko.frame)].y, move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y, move_lr[int(keiko.frame)].w,
                                            move_lr[int(keiko.frame)].h)


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
        pass

    @staticmethod
    def draw(keiko):
        if keiko.face_dir == 1:
            keiko.image.clip_draw(idle_state[int(keiko.frame)].x, idle_state[int(keiko.frame)].y, idle_state[int(keiko.frame)].w,
                                  idle_state[int(keiko.frame)].h, keiko.x, keiko.y, idle_state[int(keiko.frame)].w,
                                  idle_state[int(keiko.frame)].h)
        else:
            keiko.image.clip_composite_draw(idle_state[int(keiko.frame)].x, idle_state[int(keiko.frame)].y, idle_state[int(keiko.frame)].w,
                                            idle_state[int(keiko.frame)].h, 0, 'h', keiko.x, keiko.y, idle_state[int(keiko.frame)].w,
                                            idle_state[int(keiko.frame)].h)


class StateMachine:
    def __init__(self, keiko):
        self.keiko = keiko
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down, down_down: Up_Down, up_up: Up_Down, down_up: Up_Down},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Dia_Run, down_down: Dia_Run, up_up: Dia_Run, down_up: Dia_Run},
            Up_Down: {up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle, right_down: Dia_Run, left_down: Dia_Run, right_up: Dia_Run, left_up: Dia_Run},
            Dia_Run: {up_up: Run, down_up: Run, right_up: Up_Down, left_up: Up_Down, right_down: Up_Down, left_down: Up_Down, up_down: Run, down_down: Run}
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
                return True # 성공적으로 이벤트 변환
        return False # 이벤트를 소모하지 못했다.

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

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
