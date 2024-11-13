from frame import get_frame_size, draw_frame
from sleep import sleep


async def show_game_over(canvas, game_over_frame, max_row, max_column):
    game_over_frame_height, game_over_frame_width = get_frame_size(game_over_frame)

    while True:
        draw_frame(
            canvas=canvas,
            start_row=(max_row - game_over_frame_height) // 2,
            start_column=(max_column - game_over_frame_width) // 2,
            text=game_over_frame,
        )

        await sleep(tics=1)
