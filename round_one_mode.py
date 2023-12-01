import random

from pico2d import *

import game_framework
import physical
import select_round_mode
import server
import status_mode
from big_ball_potion import Big_Ball_Potion
from keiko import Keiko
from court import Court
from ball import Ball
from keiko_ai import Keiko_AI
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
            game_framework.change_mode(select_round_mode)
        else:
            keiko.handle_event(event)


def init():
    global court
    global keiko
    global balls
    global miyuki_ai

    court = Court()
    game_world.add_object(court, 0)

    keiko = Keiko(status_mode.state[0], status_mode.state[1])
    game_world.add_object(keiko, 2)
    game_world.add_collision_pair('keiko:ball', keiko, None)
    # game_world.add_collision_pair('keiko:power_up_item', keiko, None)
    # game_world.add_collision_pair('keiko:shrink_potion', keiko, None)
    # game_world.add_collision_pair('keiko:big_ball_potion', keiko, None)

    server.ball = Ball(480, 300, 40, 480, 300, 0)
    game_world.add_object(server.ball, 1)
    game_world.add_collision_pair('keiko:ball', None, server.ball)
    game_world.add_collision_pair('miyuki:ball', None, server.ball)

    # power_up_item = Power_Up_Item(200, 300 )
    # game_world.add_object(power_up_item, 1)
    # game_world.add_collision_pair('keiko:power_up_item', None, power_up_item)
    #
    # shrink_potion = Shrink_Potion(200, 200)
    # game_world.add_object(shrink_potion, 1)
    # game_world.add_collision_pair('keiko:shrink_potion', None, shrink_potion)
    #
    # big_ball_potion = Big_Ball_Potion(100, 200)
    # game_world.add_object(big_ball_potion, 1)
    # game_world.add_collision_pair('keiko:big_ball_potion', None, big_ball_potion)

    with open('resource/round_one_miyuki_data.json', 'rb') as f:
        miyuki_data_list = json.load(f)
        for m in miyuki_data_list:
            m["speed"] = physical.kmph_to_pps(m["speed"])
            miyuki = Miyuki()
            miyuki.__dict__.update(m)
            game_world.add_object(miyuki, 2)
            game_world.add_collision_pair('miyuki:ball', miyuki, None)
    # miyuki_ai = [Miyuki() for _ in range(3)]
    # for m in miyuki_ai:
    #     game_world.add_object(m, 2)
    #     game_world.add_collision_pair('miyuki:ball', m, None)

    keiko_ai = [Keiko_AI(status_mode.state[0], status_mode.state[1], status_mode.state[2]) for _ in range(2)]
    for k in keiko_ai:
        game_world.add_object(k, 2)
        game_world.add_collision_pair('keiko:ball', k, None)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    server.ball = None
    game_world.clear()


def resume():
    pass


def pause():
    pass