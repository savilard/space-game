import asyncio
import curses
import random
import time

from animations.fire import fire
from animations.spaceship import animate_spaceship

TIC_TIMEOUT = 0.1


def draw(canvas):
    star_count = 100
    star_symbols = '+*.:'

    max_row, max_column = curses.window.getmaxyx(canvas)

    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.refresh()

    with open('animations/frames/spaceship/frame_1.txt', 'r') as spaceship_frame_1_file:
        spaceship_frame_1 = spaceship_frame_1_file.read()

    with open('animations/frames/spaceship/frame_2.txt', 'r') as spaceship_frame_2_file:
        spaceship_frame_2 = spaceship_frame_2_file.read()

    coroutines = [
        blink(
            canvas=canvas,
            row=random.randint(2, max_row - 2),
            column=random.randint(2, max_column - 2),
            symbol=random.choice(star_symbols),
        )
        for _ in range(star_count)
    ]

    coroutines.append(fire(canvas=canvas, start_row=max_row - 2, start_column=max_column / 2))
    coroutines.append(animate_spaceship(
        canvas=canvas,
        start_row=max_row / 2,
        start_column=max_column / 2,
        spaceship_frame_1=spaceship_frame_1,
        spaceship_frame_2=spaceship_frame_2,
        max_row=max_row,
        max_column=max_column,
    ))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


async def blink(canvas, row, column, symbol='*'):
    while True:
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
