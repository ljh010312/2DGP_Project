from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN

import game_framework
import round_one_mode
import status_mode

difficulty = ['EASY', 'NORMAL', 'HARD']
difficulty_rgb = [(255,255,255), (0, 255, 0), (255, 0, 0)]
def init():
    global background
    global font
    global map
    background = load_image('resource/status_background.png')
    jp = load_image('resource/Court_Japan.png')
    id = load_image('resource/Court_India.png')
    kn = load_image('resource/Court_Kenya.png')
    map = [jp, id, kn]
    font = load_font('resource/neodgm.ttf', 50)

def finish():
    pass


def handle_events():
    global state
    global count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(status_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            for i in range(3):
                if 250 * (i + 1) - 100 < event.x < 250 * (i + 1) + 100 and 170 < 800 - 1 - event.y < 330:
                    if (i + 1) == 1:
                        game_framework.change_mode(round_one_mode)



def update():
    pass


def draw():
    clear_canvas()
    background.clip_draw(0,0, 431, 183, 512, 400, 1024, 800)
    for i in range(3):
        font.draw(250 * (i + 1) - 20, 360, f'{i + 1}', difficulty_rgb[i])
        map[i].clip_draw(0, 0, 431, 184, 250 * (i + 1), 250, 200, 160)
        font.draw(250 * (i + 1) - 50, 130, difficulty[i], difficulty_rgb[i])

    font.draw(230, 700, '난이도를 선택해주세요', (255, 255, 255))

    update_canvas()



def resume():
    pass


def pause():
    pass