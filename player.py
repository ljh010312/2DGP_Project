from pico2d import *

open_canvas()

court = load_image('Court_Japan.png')
player = load_image('Player.png')


def handle_events():
    global running, dir


    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1


running = True
x = 800 // 2
dir = 0

while running:
    clear_canvas()
    court.clip_draw(0, 0, 431, 184, 400, 300, 800, 600)
    player.clip_draw(24, 2027, 40, 75, x, 150, 50, 100)
    update_canvas()
    handle_events()
    x += dir

close_canvas()

