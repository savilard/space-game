import asyncio
import curses
import random

from sleep import sleep


async def blink(
    canvas: curses.window,
    row: int,
    column: int,
    offset_tics: int,
    symbol: str = '*',
):
    while True:

        await sleep(tics=offset_tics)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(tics=20)

        canvas.addstr(row, column, symbol)
        await sleep(tics=3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(tics=5)

        canvas.addstr(row, column, symbol)
        await sleep(tics=3)
