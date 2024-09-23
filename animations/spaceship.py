import asyncio
import itertools

from curses_tools import draw_frame


async def animate_spaceship(canvas, row, column, spaceship_frame_1, spaceship_frame_2):
    for spaceship_frame in itertools.cycle([spaceship_frame_1, spaceship_frame_2]):
        draw_frame(canvas, row, column, spaceship_frame)
        canvas.refresh()

        for _ in range(10):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, spaceship_frame, negative=True)
