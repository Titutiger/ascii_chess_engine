# Main:


"""Imports: """
import src.utils as utils

"""Variables: """
running: bool = False
mode: str = '' # pvp or pvm


"""Execution start: """

q = str(input(': ')).strip().lower()
# gets the user input in a string and splits it per `_` // (space).

if q[0] in ['s', 'start']:
    if running:
        raise ValueError('A game is already running, finish it to start another one!')
    else:
        running = True

if q[1] == 'pvm':  # player vs machine
    print('Starting pvm...')

    utils.game('pvm')

    while running:
        ...


elif q[1] == 'pvp': # player vs player
    ...