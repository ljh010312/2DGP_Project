import random

from pico2d import *

import game_framework
from keiko import Keiko
from court import Court
from ball import Ball
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
    global ball
    running = True
    world = []

    court = Court()
    game_world.add_object(court, 0)

    keiko = Keiko()
    game_world.add_object(keiko, 1)
    game_world.add_collision_pair('keiko:ball', keiko, None)

    ball = Ball(400, 300, 400, 300, 0)
    game_world.add_object(ball, 1)
    game_world.add_collision_pair('keiko:ball', None, ball)

    balls = [Ball(300, random.randint(100,300), 0, 0, 0) for _ in range(10)]
    game_world.add_objects(balls, 1)
    for b in balls:
        game_world.add_collision_pair('keiko:ball', None, b)



def update():
    game_world.update()
    game_world.handle_collisions()


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