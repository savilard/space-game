import asyncio
import curses
import itertools

from frame import draw_frame, get_frame_size
from keyboard.controls import read_controls


async def animate_spaceship(
    canvas: curses.window,
    start_row: int,
    start_column: int,
    spaceship_frame_1: str,
    spaceship_frame_2: str,
    max_row: int,
    max_column: int,
    screen_border: int = 2,
):
    row, column = start_row, start_column

    for spaceship_frame in itertools.cycle([spaceship_frame_1, spaceship_frame_2]):
        spaceship_frame_height, spaceship_frame_width = get_frame_size(spaceship_frame)

        row = min(max(screen_border, row), max_row - spaceship_frame_height)
        column = min(max(screen_border, column), max_column - spaceship_frame_width)

        draw_frame(canvas, row, column, spaceship_frame)
        canvas.refresh()

        for _ in range(2):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, spaceship_frame, negative=True)

        rows_direction, columns_direction, space_pressed = read_controls(canvas=canvas)

        row += rows_direction
        column += columns_direction
