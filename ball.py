from pico2d import *
import game_world
import game_framework


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, target_x = 400, target_y = 300, power = 0):
        if Ball.image == None:
            Ball.image = load_image('ball.png')
        self.x, self.y= x, y
        self.target_x, self.target_y = target_x, target_y
        self.power = power
        self.direction = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.decay_rate = 0.02

    def draw(self):
        self.image.clip_draw(3, 51, 26, 26, self.x, self.y, 20, 20)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.power * 30 * math.cos(self.direction) * game_framework.frame_time
        self.y += self.power * 30 * math.sin(self.direction) * game_framework.frame_time

        self.power -= self.decay_rate
        self.power = clamp(0, self.power, 30)
        if self.x < 25 or self.x > 1024 - 25:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            pass


class Big_Ball:
    image = None

    def __init__(self, x = 400, y = 300, target_x = 400, target_y = 300, power = 0):
        if Big_Ball.image == None:
            Big_Ball.image = load_image('ball.png')
        self.x, self.y= x, y
        self.target_x, self.target_y = target_x, target_y
        self.power = power
        self.direction = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.decay_rate = 0.02


    def draw(self):
        self.image.clip_draw(3, 51, 26, 26, self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.power * 30 * math.cos(self.direction) * game_framework.frame_time
        self.y += self.power * 30 * math.sin(self.direction) * game_framework.frame_time

        self.power -= self.decay_rate
        self.power = clamp(0, self.power, 30)
        if self.x < 25 or self.x > 1024 - 25:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            pass

