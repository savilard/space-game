import curses


def draw_frame(  # noqa: WPS210
    canvas: curses.window,
    start_row: int,
    start_column: int,
    text: str,
    negative: bool = False,
):
    """
    Draw multiline text fragment on canvas.

    Erase text instead of drawing if negative=True is specified.
    """
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = ' ' if negative else symbol
            canvas.addch(row, column, symbol)


def get_frame_size(text: str):
    """Calculate size of multiline text fragment.

    Args:
        text:  multiline text fragment

    Returns:
        tuple: pair — number of rows and columns
    """
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns
