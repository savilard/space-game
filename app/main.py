import curses
import functools

from draw import draw


def main():
    curses.update_lines_cols()
    curses.wrapper(
        functools.partial(
            draw,
            star_count=100,
            star_symbols='+*.:',
            tic_timeout=0.1,
        ),
    )


if __name__ == '__main__':
    main()
