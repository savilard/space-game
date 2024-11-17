from global_vars import YEARS
from sleep import sleep

PHRASES = {
    1957: 'First Sputnik',
    1961: 'Gagarin flew!',
    1969: 'Armstrong got on the moon!',
    1971: 'First orbital space station Salute-1',
    1981: 'Flight of the Shuttle Columbia',
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: 'Take the plasma gun! Shoot the garbage!',
}


async def show_current_year(canvas):
    year_row_position = 1
    year_column_position = 1

    while True:
        message = f'Year now: {YEARS['year']} - {PHRASES.get(YEARS['year'], '')}'
        canvas.addstr(year_row_position, year_column_position, message)
        await sleep(15)
        YEARS['year'] += 1
        canvas.refresh()
