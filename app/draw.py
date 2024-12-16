import curses
import random
import time
from pathlib import Path

from animations.blink import blink
from animations.current_year import show_current_year
from animations.space_garbage import fill_orbit_with_garbage
from animations.spaceship import animate_spaceship
from global_vars import OBSTACLES
from obstacles import show_obstacles


def draw(
    canvas: curses.window,
    star_count: int,
    star_symbols: str,
    tic_timeout: float,
):
    curses.curs_set(False)

    max_row, max_column = curses.window.getmaxyx(canvas)

    text_canvas_height = 3

    game_canvas = canvas.derwin(max_row - text_canvas_height, max_column, 0, 0)
    game_canvas.nodelay(True)
    game_canvas.border()
    game_canvas.keypad(True)
    game_canvas_max_row, game_canvas_max_column = game_canvas.getmaxyx()

    text_canvas = canvas.derwin(text_canvas_height, max_column, max_row - text_canvas_height, 0)
    text_canvas.nodelay(True)

    spaceship_frame1_path = Path.cwd() / 'app' / 'animations' / 'frames' / 'spaceship' / 'frame_1.txt'
    spaceship_frame2_path = Path.cwd() / 'app' / 'animations' / 'frames' / 'spaceship' / 'frame_2.txt'

    garbage_frames_folder = Path.cwd() / 'app' / 'animations' / 'frames' / 'space_garbage'
    garbage_frames_path = [frame_path for frame_path in Path(garbage_frames_folder).rglob('*.txt')]

    game_over_frame_path = Path.cwd() / 'app' / 'animations' / 'frames' / 'game_over.txt'

    screen_border_width = 2

    with open(spaceship_frame1_path, 'r') as spaceship_frame1_file:
        spaceship_frame1 = spaceship_frame1_file.read()

    with open(spaceship_frame2_path) as spaceship_frame2_file:
        spaceship_frame2 = spaceship_frame2_file.read()

    with open(game_over_frame_path) as game_over_frame_file:
        game_over_frame = game_over_frame_file.read()

    coroutines = [
        blink(
            canvas=game_canvas,
            row=random.SystemRandom().randint(screen_border_width, game_canvas_max_row - screen_border_width),
            column=random.SystemRandom().randint(screen_border_width, game_canvas_max_column - screen_border_width),
            symbol=random.SystemRandom().choice(star_symbols),
            offset_tics=random.randint(1, 20),
        )
        for _ in range(star_count)
    ]

    coroutines.append(
        animate_spaceship(
            coroutines=coroutines,
            canvas=game_canvas,
            spaceship_frame1=spaceship_frame1,
            spaceship_frame2=spaceship_frame2,
            max_row=game_canvas_max_row,
            max_column=game_canvas_max_column,
            screen_border_width=screen_border_width,
            game_over_frame=game_over_frame,
        ),
    )
    coroutines.append(
        fill_orbit_with_garbage(
            coroutines=coroutines,
            canvas=game_canvas,
            garbage_frames_path=garbage_frames_path,
            max_column=game_canvas_max_column,
            screen_border_width=screen_border_width,
        )
    )
    coroutines.append(show_current_year(canvas=text_canvas))

    while True:  # noqa: WPS457
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break

        game_canvas.refresh()

        time.sleep(tic_timeout)
