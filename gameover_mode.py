from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN

import game_framework
import round_one_mode
import select_round_mode
import status_mode


def init():
    global image
    global font
    global bgm
    bgm = load_music('resource/gameover.mp3')
    bgm.set_volume(32)
    bgm.play()
    image = load_image('resource/gameover.png')
    font = load_font('resource/neodgm.ttf', 50)


def finish():
    bgm.stop()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_MOUSEBUTTONDOWN:
            if 870 < event.x < 1024 and 0 < 800 - 1 - event.y < 50:
                game_framework.change_mode(select_round_mode)
            if 30 < event.x < 230 and 0 < 800 - 1 - event.y < 50:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(select_round_mode)


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 10, 304, 224, 512, 400, 1024, 800)
    font.draw(30, 50, 'EXIT', (255, 255, 255))
    font.draw(870, 50, 'RETRY', (255, 255, 255))
    update_canvas()


def resume():
    pass


def pause():
    pass
