from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import round_one_mode
import status_mode


def init():
    global image
    global font
    global bgm
    bgm = load_music('resource/title.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    image = load_image('resource/title.png')
    font = load_font('resource/neodgm.ttf', 100)


def finish():
    bgm.stop()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(status_mode)


def update():
    pass


def draw():
    clear_canvas()
    image.draw(512, 400, 1024, 800)
    font.draw(320, 200, '피구 왕', (0, 0, 0))
    font.draw(10, 100, 'Press Space to Start', (0, 0, 0))

    update_canvas()


def resume():
    pass


def pause():
    pass
