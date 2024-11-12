import asyncio
import curses
import random

from frame import draw_frame, get_frame_size
from global_vars import OBSTACLES, OBSTACLES_IN_LAST_COLLISIONS
from obstacles import Obstacle, has_collision
from sleep import sleep


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    rows_size, columns_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, rows_size, columns_size)
    OBSTACLES.append(obstacle)

    try:
        while row < rows_number:

            if obstacle in OBSTACLES_IN_LAST_COLLISIONS:
                OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
                return None

            draw_frame(canvas, row, column, garbage_frame)
            obstacle.row = row
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
    finally:
        OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(
    coroutines,
    canvas: curses.window,
    garbage_frames_path: list[str],
    max_column: int,
    screen_border_width: int,
    offset_tics: int,
):
    while True:
        random_garbage_frame_path = random.SystemRandom().choice(garbage_frames_path)

        with open(random_garbage_frame_path, 'r') as garbage_file:
            garbage_frame = garbage_file.read()

        await sleep(tics=offset_tics)

        column = random.SystemRandom().randint(screen_border_width, max_column)

        coroutines.append(
            fly_garbage(canvas, column=column, garbage_frame=garbage_frame)
        )
