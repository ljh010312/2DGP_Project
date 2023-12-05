from pico2d import load_image


# 코트는 가로 22m 세로 8m
class Court:
    def __init__(self):
        self.court_num = 1
        self.japan = load_image('resource/Court_Japan.png')
        self.india = load_image('resource/Court_India.png')
        self.kenya = load_image('resource/Court_Kenya.png')

    def draw(self):
        if self.court_num == 1:
            self.japan.clip_draw(0, 0, 431, 184, 512, 400, 1024, 800)
        elif self.court_num == 2:
            self.india.clip_draw(0, 0, 431, 184, 512, 400, 1024, 800)
        else:
            self.kenya.clip_draw(0, 0, 431, 184, 512, 400, 1024, 800)

    def update(self):
        pass
