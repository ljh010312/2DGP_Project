from pico2d import load_image


class Idle:
    @staticmethod
    def do():
        print('드르렁... Zz.z.....')

    @staticmethod
    def enter():
        print('고개 숙이기')

    @staticmethod
    def exit():
        print('눈 뜨기')

    @staticmethod
    def draw():
        print('인건')


class StateMachine:
    def __init__(self):
        self.cur_state = Idle
        pass

    def start(self):
        self.cur_state.enter()
        pass

    def update(self):
        self.cur_state.do()
        pass

    def draw(self):
        self.cur_state.draw()
        pass

    pass



class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('player.png')
        self.state_machine = StateMachine()
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.image.clip_draw(24, 2027, 40, 75, self.x, 150, 50, 100)
        self.state_machine.draw()