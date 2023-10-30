from pico2d import load_image


class Court:
    def __init__(self):
        self.image = load_image('Court_Japan.png')

    def draw(self):
        self.image.clip_draw(0, 0, 431, 184, 400, 300, 800, 600)

    def update(self):
        pass
