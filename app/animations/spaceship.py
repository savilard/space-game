import asyncio
import curses
import itertools

from animations.fire import fire
from animations.game_over import show_game_over
from frame import draw_frame, get_frame_size
from global_vars import OBSTACLES
from keyboard.controls import read_controls
from obstacles import has_collision
from physics import update_speed


async def animate_spaceship(
    coroutines,
    canvas: curses.window,
    spaceship_frame1: str,
    spaceship_frame2: str,
    max_row: int,
    max_column: int,
    screen_border_width: int,
    game_over_frame: str,
):
    row = max_row / 2
    column = max_column / 2

    row_speed = column_speed = 0

    spaceship_frames = [spaceship_frame1, spaceship_frame1, spaceship_frame2, spaceship_frame2]

    for spaceship_frame in itertools.cycle(spaceship_frames):
        spaceship_frame_height, spaceship_frame_width = get_frame_size(spaceship_frame)

        row = min(max(screen_border_width, row), max_row - spaceship_frame_height)
        column = min(max(screen_border_width, column), max_column - spaceship_frame_width)

        for obstacle in OBSTACLES:
            is_has_collision = has_collision(
                (obstacle.row, obstacle.column),
                (obstacle.rows_size, obstacle.columns_size),
                (row, column),
            )
            if is_has_collision:
                coroutines.append(
                    show_game_over(
                        canvas=canvas,
                        max_row=max_row,
                        max_column=max_column,
                        game_over_frame=game_over_frame,
                    )
                )
                return None

        draw_frame(canvas, row, column, spaceship_frame)

        await asyncio.sleep(0)

        draw_frame(canvas, row, column, spaceship_frame, negative=True)

        rows_direction, columns_direction, space_pressed = read_controls(canvas=canvas)

        if space_pressed:
            coroutines.append(
                fire(
                    canvas=canvas,
                    start_row=row,
                    start_column=column + screen_border_width,
                ),
            )

        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction,
        )

        row += row_speed
        column += column_speed
