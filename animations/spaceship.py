import asyncio
import itertools

from curses_tools import draw_frame, read_controls


async def animate_spaceship(canvas, start_row, start_column, spaceship_frame_1, spaceship_frame_2):
    row, column = start_row, start_column

    for spaceship_frame in itertools.cycle([spaceship_frame_1, spaceship_frame_2]):
        draw_frame(canvas, row, column, spaceship_frame)
        canvas.refresh()

        for _ in range(2):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, spaceship_frame, negative=True)

        rows_direction, columns_direction, space_pressed = read_controls(canvas=canvas)

        row += rows_direction
        column += columns_direction
