from pico2d import *

class Shrink_Potion:
    image = None

    def __init__(self, x = 400, y = 300):
        if Shrink_Potion.image == None:
            Shrink_Potion.image = load_image('item.png')
        self.x, self.y= x, y

    def draw(self):
        self.image.clip_draw(408, 399, 63, 82, self.x, self.y, 20, 25)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 12, self.x + 10, self.y + 12

    def handle_collision(self, group, other):
        pass