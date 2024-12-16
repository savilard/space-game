import asyncio
import curses
import random

from animations.explosion import explode
from frame import draw_frame, get_frame_size
from game_scenario import get_garbage_delay_tics
from global_vars import OBSTACLES, OBSTACLES_IN_LAST_COLLISIONS, YEARS
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

                await explode(canvas, row + rows_size // 2, column + columns_size // 2)

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
):
    while True:
        await asyncio.sleep(0)

        offset_tics = get_garbage_delay_tics(year=YEARS['year'])
        if offset_tics is None:
            continue

        await sleep(tics=offset_tics)

        random_garbage_frame_path = random.SystemRandom().choice(garbage_frames_path)
        with open(random_garbage_frame_path, 'r') as garbage_file:
            garbage_frame = garbage_file.read()

        column = random.SystemRandom().randint(screen_border_width, max_column)
        coroutines.append(
            fly_garbage(canvas, column=column, garbage_frame=garbage_frame)
        )
