import asyncio
import curses
import time

TIC_TIMEOUT = 0.1


def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    curses.curs_set(False)
    canvas.refresh()

    coroutines = [
        blink(canvas, row, 5),
        blink(canvas, row, 10),
        blink(canvas, row, 15),
        blink(canvas, row, 20),
        blink(canvas, row, 25),
    ]

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
