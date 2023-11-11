from pico2d import *

import game_framework
from keiko import Keiko
from court import Court
import game_world

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            keiko.handle_event(event)


def init():
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


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()


def resume():
    pass


def pause():
    pass