from pico2d import *
import game_world
import game_framework


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_draw(3, 51, 26, 26, self.x, self.y, 20, 20)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 800 - 25:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            game_world.remove_object(self)
