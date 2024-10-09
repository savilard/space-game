import curses
import random
import time
from pathlib import Path

from animations.blink import blink
from animations.fire import fire
from animations.spaceship import animate_spaceship


def draw(
    canvas: curses.window,
    star_count: int,
    star_symbols: str,
    tic_timeout: float,
):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.refresh()

    spaceship_frame1_path = Path.cwd() / 'app' / 'animations' / 'frames' / 'spaceship' / 'frame_1.txt'
    spaceship_frame2_path = Path.cwd() / 'app' / 'animations' / 'frames' / 'spaceship' / 'frame_2.txt'

    with open(spaceship_frame1_path, 'r') as spaceship_frame_1_file:
        spaceship_frame_1 = spaceship_frame_1_file.read()

    with open(spaceship_frame2_path) as spaceship_frame_2_file:
        spaceship_frame_2 = spaceship_frame_2_file.read()

    max_row, max_column = curses.window.getmaxyx(canvas)

    coroutines = [
        blink(
            canvas=canvas,
            row=random.SystemRandom().randint(2, max_row - 2),
            column=random.SystemRandom().randint(2, max_column - 2),
            symbol=random.SystemRandom().choice(star_symbols),
        )
        for _ in range(star_count)
    ]

    coroutines.append(
        fire(
            canvas=canvas,
            start_row=max_row - 2,
            start_column=max_column / 2,
        ),
    )
    coroutines.append(
        animate_spaceship(
            canvas=canvas,
            start_row=max_row / 2,
            start_column=max_column / 2,
            spaceship_frame_1=spaceship_frame_1,
            spaceship_frame_2=spaceship_frame_2,
            max_row=max_row,
            max_column=max_column,
        ),
    )

    while True:  # noqa: WPS457
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break
        canvas.refresh()
        time.sleep(tic_timeout)
