from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font, load_music, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN

import game_framework
import round_one_mode
import select_round_mode
import server
import title_mode
from keiko_ai import catch_motion, throw_motion, move_lr
from physical import FRAMES_PER_ACTION, ACTION_PER_TIME

motion = [move_lr, throw_motion, catch_motion]
state_list = ['속도', '파워', '순발력']
def init():
    global background
    global status
    global font
    global count
    global keiko
    global frame
    global state
    global bgm
    global up, down
    up = load_wav('resource/up.wav')
    up.set_volume(50)
    down = load_wav('resource/down.wav')
    down.set_volume(50)
    bgm = load_music('resource/status.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    status = load_image('resource/status.png')
    background = load_image('resource/status_background.png')
    font = load_font('resource/neodgm.ttf', 50)
    keiko = load_image('resource/keiko.png')
    count = server.count
    state = [0, 0, 0]
    frame = 0

def finish():
    bgm.stop()
    pass


def handle_events():
    global state
    global count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if 870 < event.x < 1024 and 0 < 800 - 1-event.y < 50:
                game_framework.change_mode(select_round_mode)
            if 30 < event.x < 230 and 0 < 800 - 1- event.y < 50:
                game_framework.change_mode(title_mode)
            for i in range(3):
                if 200 * (i + 1) < event.x < 300 * (i + 1):
                    if 450 < 800 - 1 - event.y < 550:
                        if count <= 0: break
                        if state[i] >= 10: break
                        up.play()
                        state[i] += 1
                        count -= 1
                    elif 50 < 800 - 1 - event.y < 150:
                        if count >= 10: break
                        if state[i] <= 0: break
                        down.play()
                        state[i] -= 1
                        count += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(select_round_mode)


def update():
    global frame
    frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


def draw():
    clear_canvas()
    background.clip_draw(0,0, 431, 183, 512, 400, 1024, 800)
    font.draw(300, 700, '스탯을 올려주세요', (255, 255, 255))
    font.draw(10, 300, '포인트', (0, 0, 0))
    font.draw(60, 230, f'{count}', (0,0,0))
    font.draw(30, 50, 'BACK', (255, 255, 255))
    font.draw(870, 50, 'START', (255,255,255))
    for i in range(3):
        status.clip_draw(98, 1, 28, 30, 250 * (i + 1), 500, 100, 100)
        status.clip_draw(163, 1, 26, 30, 250 * (i + 1), 100, 100, 100)
        font.draw(250 * (i + 1) - 50, 400, state_list[i], (0,0,0))
        font.draw(250 * (i + 1), 200, f'{state[i]}', (0,0,0))

        keiko.clip_draw(motion[i][int(frame)].x, motion[i][int(frame)].y,
                                        motion[i][int(frame)].w,
                                        motion[i][int(frame)].h, 250 * (i + 1), 300,
                                        motion[i][int(frame)].w * 2,
                                        motion[i][int(frame)].h * 2)

    update_canvas()



def resume():
    pass


def pause():
    pass