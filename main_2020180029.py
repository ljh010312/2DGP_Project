from pico2d import open_canvas, close_canvas
import game_framework
# import round_one_mode as start_mode
# import select_round_mode as start_mode
import title_mode as start_mode
# import status_mode as start_mode
# import gameover_mode as start_mode

open_canvas(1024, 800)
game_framework.run(start_mode)
close_canvas()
