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
    year = 1957

    while True:
        message = f'Year now: {year} - {PHRASES.get(year, '')}'

        canvas.addstr(0, 0, message)
        await sleep(15)

        year += 1
        YEARS['year'] = year

        canvas.refresh()
