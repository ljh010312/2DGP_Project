import random
import tomllib

from pico2d import *

import game_framework
import gameover_mode
import physical
import select_round_mode
import server
import status_mode
import win_mode
from keiko import Keiko
from court import Court
from ball import Ball
from keiko_ai import Keiko_AI
from miyuki import Miyuki
import game_world
from power_up_item import Power_Up_Item
from shrink_potion import Shrink_Potion
from big_ball_potion import Big_Ball_Potion


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_round_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            keiko_out()
        else:
            keiko.handle_event(event)


def init():
    global court
    global keiko
    global balls
    global miyuki_ai
    global bgm
    bgm = load_music('resource/2_Stage.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    with open('resource/round_two_data.toml', 'rb') as f:
        court_data_list = tomllib.load(f)['court']
        for c in court_data_list:
            court = Court()
            court.__dict__.update(c)
            game_world.add_object(court, 0)

    keiko = Keiko(speed=status_mode.state[0], power=status_mode.state[1], catch_percentage=status_mode.state[2])
    game_world.add_object(keiko, 2)
    game_world.add_collision_pair('keiko:ball', keiko, None)

    server.ball = Ball(480, 300, 40, 480, 300, 0)
    game_world.add_object(server.ball, 1)
    game_world.add_collision_pair('keiko:ball', None, server.ball)
    game_world.add_collision_pair('miyuki:ball', None, server.ball)

    power_up_item = Power_Up_Item(100, 30)
    game_world.add_object(power_up_item, 1)

    shrink_potion = Shrink_Potion(150, 30)
    game_world.add_object(shrink_potion, 1)

    big_ball_potion = Big_Ball_Potion(200, 30)
    game_world.add_object(big_ball_potion, 1)

    with open('resource/round_two_data.toml', 'rb') as f:
        miyuki_data_list = tomllib.load(f)['miyuki']
        for m in miyuki_data_list:
            m["speed"] = physical.kmph_to_pps(m["speed"])
            miyuki = Miyuki()
            miyuki.__dict__.update(m)
            game_world.add_object(miyuki, 2)
            game_world.add_collision_pair('miyuki:ball', miyuki, None)

    keiko_ai = [Keiko_AI(status_mode.state[0], status_mode.state[1], status_mode.state[2]) for _ in range(2)]
    for k in keiko_ai:
        game_world.add_object(k, 2)
        game_world.add_collision_pair('keiko:ball', k, None)


def update():
    game_world.update()
    game_world.handle_collisions()
    win_or_lose()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    bgm.stop()
    server.ball = None
    game_world.clear()


def resume():
    pass


def pause():
    pass


def win_or_lose():
    keiko_count = 0
    miyuki_count = 0
    for layer in game_world.objects:
        for o in layer:
            if isinstance(o, Keiko_AI) or isinstance(o, Keiko):
                keiko_count += 1
            elif isinstance(o, Miyuki):
                miyuki_count += 1
    if keiko_count == 0:
        game_framework.change_mode(gameover_mode)

    if miyuki_count == 0:
        server.count += 3
        game_framework.change_mode(win_mode)


def keiko_out():
    global keiko
    keiko_live = False
    keiko_ai_live = False
    temp = None
    for layer in game_world.objects:
        for o in layer:
            if isinstance(o, Keiko_AI):
                if o.state == 'Walk':
                    temp = o
                    keiko_ai_live = True
            if isinstance(o, Keiko):
                keiko_live = True

    if not keiko_live:
        if keiko_ai_live:
            keiko = Keiko(x=temp.x, y=temp.y, speed=status_mode.state[0], power=status_mode.state[1],
                          catch_percentage=status_mode.state[2])
            game_world.add_object(keiko, 2)
            game_world.add_collision_pair('keiko:ball', keiko, None)
            game_world.remove_object(temp)
