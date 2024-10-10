import curses

from keyboard.codes import KeyboardCodes


def read_controls(canvas: curses.window):
    """Read keys pressed and returns tuple with controls state."""
    rows_direction = 0
    columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        match pressed_key_code:
            case -1:
                # https://docs.python.org/3/library/curses.html#curses.window.getch
                break
            case KeyboardCodes.up_key_code:
                rows_direction = -1
            case KeyboardCodes.down_key_code:
                rows_direction = 1
            case KeyboardCodes.right_key_code:
                columns_direction = 1
            case KeyboardCodes.left_key_code:
                columns_direction = -1
            case KeyboardCodes.space_key_code:
                space_pressed = True

    return rows_direction, columns_direction, space_pressed
