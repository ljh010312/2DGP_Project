from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
GRAVITY_SPEED_KMPH = -10.0  # Km / Hour
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)

Z_SPEED_KMPH = 10.0  # Km / Hour
Z_SPEED_MPM = (Z_SPEED_KMPH * 1000.0 / 60.0)
Z_SPEED_MPS = (Z_SPEED_MPM / 60.0)
Z_SPEED_PPS = (Z_SPEED_MPS * PIXEL_PER_METER)


class Ball:
    image = None
    shadow_image = None

    def __init__(self, x = 400, y = 300, z = 40,  target_x = 400, target_y = 300, power = 0):
        if Ball.image == None:
            Ball.image = load_image('ball.png')
        if Ball.shadow_image == None:
            Ball.shadow_image = load_image('shadow.png')

        self.x, self.y, self.z = x, y, z
        self.shadow_y = y - z
        self.z_speed = 0
        self.target_x, self.target_y = target_x, target_y
        self.power = power
        self.direction = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.decay_rate = 0.01
        self.shadow_scale = 1
        self.state = 'Stay'



    def draw(self):
        if not self.state == 'Hold':
            self.shadow_image.clip_draw(90, 157, 844, 144, self.x, self.shadow_y, 25 * self.shadow_scale, 15* self.shadow_scale)
        self.image.clip_draw(3, 51, 26, 26, self.x, self.y, 20, 20)

        draw_rectangle(*self.get_bb())


    def update(self):
        self.x += self.power * 30 * math.cos(self.direction) * game_framework.frame_time
        self.z += self.z_speed * game_framework.frame_time
        self.y += self.power * 30 * math.sin(self.direction) * game_framework.frame_time + self.z_speed * game_framework.frame_time
        self.shadow_y = self.y - self.z - 10
        self.z_speed += GRAVITY_SPEED_PPS * game_framework.frame_time
        self.shadow_scale = 1 - (self.z / 50)
        if self.z < 0:
            self.bound()


        if (self.state == 'KeikoThrow' or self.state == 'Throw') and self.power == 0:
            self.state = 'Stay'

        if self.x < 25:
            self.x, self.y = 200, 100

        if self.x > 1024 - 25:
            self.x, self.y = 400, 100

    def bound(self):
        bound_decay = 2
        set_stop = 2

        self.z = 0.0
        self.z_speed = abs(self.z_speed / bound_decay)
        self.power = self.power / bound_decay
        if abs(self.z_speed) < set_stop: self.z_speed = 0.0
        if self.power < set_stop: self.power = 0.0

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'keiko:ball':
            pass
        elif group == 'miyuki:ball':
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

