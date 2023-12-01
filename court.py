from pico2d import load_image

# 코트는 가로 22m 세로 8m
class Court:
    def __init__(self):
        self.image = load_image('Court_Japan.png')

    def draw(self):
        self.image.clip_draw(0, 0, 431, 184, 512, 400, 1024, 800)

    def update(self):
        pass
