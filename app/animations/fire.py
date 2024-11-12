import asyncio
import curses

from global_vars import OBSTACLES, OBSTACLES_IN_LAST_COLLISIONS
from obstacles import has_collision


async def fire(
    canvas: curses.window,
    start_row: int,
    start_column: int,
    rows_speed: float = -0.3,
    columns_speed: int = 0,
):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    for obstacle in OBSTACLES:
        is_has_collision = has_collision(
            (obstacle.row, obstacle.column),
            (obstacle.rows_size, obstacle.columns_size),
            (row, column),
        )
        if is_has_collision:
            OBSTACLES_IN_LAST_COLLISIONS.append(obstacle)
            return None

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
