# Game file.


def game(mode: str) -> str:
    valid_mode: bool = False
    if mode in ['pvm', 'pvp']:
        valid_mode = True

    if valid_mode:
        ...
