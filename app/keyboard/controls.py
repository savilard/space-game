from keyboard.codes import KeyboardCodes


def read_controls(canvas):
    """Read keys pressed and returns tuple with controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        match pressed_key_code:
            case -1:
                # https://docs.python.org/3/library/curses.html#curses.window.getch
                break
            case KeyboardCodes.UP_KEY_CODE:
                rows_direction = -1
            case KeyboardCodes.DOWN_KEY_CODE:
                rows_direction = 1
            case KeyboardCodes.RIGHT_KEY_CODE:
                columns_direction = 1
            case KeyboardCodes.LEFT_KEY_CODE:
                columns_direction = -1
            case KeyboardCodes.SPACE_KEY_CODE:
                space_pressed = True

    return rows_direction, columns_direction, space_pressed
