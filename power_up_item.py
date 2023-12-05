from pico2d import *


class Power_Up_Item:
    image = None

    def __init__(self, x=400, y=300):
        if Power_Up_Item.image == None:
            Power_Up_Item.image = load_image('resource/item.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.clip_draw(19, 399, 63, 82, self.x, self.y, 40, 50)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 12, self.x + 10, self.y + 12

    def handle_collision(self, group, other):
        pass
