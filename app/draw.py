import curses
import random
import time
from pathlib import Path

from animations.blink import blink
from animations.space_garbage import fill_orbit_with_garbage
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

    garbage_frames_folder = Path.cwd() / 'app' / 'animations' / 'frames' / 'space_garbage'
    garbage_frames_path = [frame_path for frame_path in Path(garbage_frames_folder).rglob('*.txt')]

    screen_border_width = 2

    with open(spaceship_frame1_path, 'r') as spaceship_frame1_file:
        spaceship_frame1 = spaceship_frame1_file.read()

    with open(spaceship_frame2_path) as spaceship_frame2_file:
        spaceship_frame2 = spaceship_frame2_file.read()

    max_row, max_column = curses.window.getmaxyx(canvas)

    coroutines = [
        blink(
            canvas=canvas,
            row=random.SystemRandom().randint(screen_border_width, max_row - screen_border_width),
            column=random.SystemRandom().randint(screen_border_width, max_column - screen_border_width),
            symbol=random.SystemRandom().choice(star_symbols),
            offset_tics=random.randint(1, 20),
        )
        for _ in range(star_count)
    ]

    coroutines.append(
        animate_spaceship(
            coroutines=coroutines,
            canvas=canvas,
            spaceship_frame1=spaceship_frame1,
            spaceship_frame2=spaceship_frame2,
            max_row=max_row,
            max_column=max_column,
            screen_border_width=screen_border_width,
        ),
    )
    coroutines.append(
        fill_orbit_with_garbage(
            coroutines=coroutines,
            canvas=canvas,
            garbage_frames_path=garbage_frames_path,
            max_column=max_column,
            screen_border_width=screen_border_width,
            offset_tics=random.randint(1, 50),
        )
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
