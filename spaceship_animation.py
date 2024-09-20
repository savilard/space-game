import asyncio
import itertools

from curses_tools import draw_frame


async def animate_spaceship(canvas, row, column, rocket_frame_1, rocket_frame_2):
    for rocket_frame in itertools.cycle([rocket_frame_1, rocket_frame_2]):
        draw_frame(canvas, row, column, rocket_frame)
        canvas.refresh()

        for _ in range(10):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, rocket_frame, negative=True)
