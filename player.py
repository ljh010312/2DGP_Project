# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_d, SDLK_a, SDLK_w, SDLK_s


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
    def enter(player, e):
        player.frame = 0
        if up_down(e) or down_up(e):
            player.dir = 1
        elif down_down(e) or up_up(e):
            player.dir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.y += player.dir * 5

    @staticmethod
    def draw(player):
        if player.face_dir > 0:
            player.image.clip_draw(move_lr[player.frame].x, move_lr[player.frame].y, move_lr[player.frame].w, move_lr[player.frame].h, player.x, player.y,  move_lr[player.frame].w, move_lr[player.frame].h)
        else:
            player.image.clip_composite_draw(move_lr[player.frame].x, move_lr[player.frame].y, move_lr[player.frame].w,
                                   move_lr[player.frame].h, 0, 'h', player.x, player.y, move_lr[player.frame].w,
                                   move_lr[player.frame].h)


class Run:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):
            player.dir, player.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            player.dir, player.face_dir = -1, -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.dir * 5

    @staticmethod
    def draw(player):
        if player.dir > 0:
            player.image.clip_draw(move_lr[player.frame].x, move_lr[player.frame].y, move_lr[player.frame].w, move_lr[player.frame].h, player.x, player.y,  move_lr[player.frame].w, move_lr[player.frame].h)
        else:
            player.image.clip_composite_draw(move_lr[player.frame].x, move_lr[player.frame].y, move_lr[player.frame].w,
                                   move_lr[player.frame].h, 0, 'h', player.x, player.y, move_lr[player.frame].w,
                                   move_lr[player.frame].h)



class Idle:
    @staticmethod
    def enter(player, e):
        player.dir = 0
        player.frame = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(idle_state[player.frame].x, idle_state[player.frame].y, idle_state[player.frame].w, idle_state[player.frame].h, player.x, player.y, idle_state[player.frame].w, idle_state[player.frame].h)
        else:
            player.image.clip_composite_draw(idle_state[player.frame].x, idle_state[player.frame].y, idle_state[player.frame].w,
                                   idle_state[player.frame].h, 0, 'h', player.x, player.y, idle_state[player.frame].w,
                                   idle_state[player.frame].h)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down: Up_Down, down_down: Up_Down, up_up: Up_Down, down_up: Up_Down},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Up_Down: {up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True # 성공적으로 이벤트 변환
        return False # 이벤트를 소모하지 못했다.

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('player.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
