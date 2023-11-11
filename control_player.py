from pico2d import *
from keiko import Keiko
from court import Court
import game_world

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            keiko.handle_event(event)


def reset_world():
    global running
    global court
    global keiko
    global world

    running = True
    world = []

    court = Court()
    game_world.add_object(court, 0)

    keiko = Keiko()
    game_world.add_object(keiko, 1)


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()