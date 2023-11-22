import random

from pico2d import *

import game_framework
from big_ball_potion import Big_Ball_Potion
from keiko import Keiko
from court import Court
from ball import Ball
from miyuki import Miyuki
import game_world
from power_up_item import Power_Up_Item
from shrink_potion import Shrink_Potion


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            print(event.x, event.y)
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
    game_world.add_object(keiko, 2)
    game_world.add_collision_pair('keiko:ball', keiko, None)
    game_world.add_collision_pair('keiko:power_up_item', keiko, None)
    game_world.add_collision_pair('keiko:shrink_potion', keiko, None)
    game_world.add_collision_pair('keiko:big_ball_potion', keiko, None)

    ball = Ball(400, 300, 400, 300, 0)
    game_world.add_object(ball, 1)
    game_world.add_collision_pair('keiko:ball', None, ball)

    balls = [Ball(300, random.randint(100,300), 0, 0, 0) for _ in range(10)]
    game_world.add_objects(balls, 1)
    for b in balls:
        game_world.add_collision_pair('keiko:ball', None, b)

    power_up_item = Power_Up_Item(200, 300 )
    game_world.add_object(power_up_item, 1)
    game_world.add_collision_pair('keiko:power_up_item', None, power_up_item)

    shrink_potion = Shrink_Potion(200, 200)
    game_world.add_object(shrink_potion, 1)
    game_world.add_collision_pair('keiko:shrink_potion', None, shrink_potion)

    big_ball_potion = Big_Ball_Potion(100, 200)
    game_world.add_object(big_ball_potion, 1)
    game_world.add_collision_pair('keiko:big_ball_potion', None, big_ball_potion)

    miyuki = Miyuki()
    game_world.add_object(miyuki, 2)


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