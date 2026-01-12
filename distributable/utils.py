import shutil
from typing import Tuple

import colorama

import sys
USE_COLOR = True
colorama.init()

class Colors:
    INFO = colorama.Fore.YELLOW if USE_COLOR else ""
    PATH = colorama.Fore.BLUE if USE_COLOR else ""
    SUCCESS = colorama.Fore.GREEN if USE_COLOR else ""
    ERROR = colorama.Fore.RED if USE_COLOR else ""
    WARNING = colorama.Fore.MAGENTA if USE_COLOR else ""
    HASH = colorama.Fore.CYAN if USE_COLOR else ""
    RESET = colorama.Style.RESET_ALL if USE_COLOR else ""
    HUH = colorama.Fore.LIGHTYELLOW_EX if USE_COLOR else ""


# ANSI escape codes for blinking and reset
BLINK = '\033[5m'
RESET = '\033[0m'

title: str = 'TermiChess'
authors: str = 'Aarin & Ojas'
lic: str = 'Null'

inception: str = 'Null'
v_dev: str = '1.0.0'
v_usr: str = '1.0'

def get_terminal_size() -> Tuple[int, int]:
    """
    Safely get terminal size, capped at (80, 24).
    """
    try:
        columns, rows = shutil.get_terminal_size()
        return min(columns, 80), min(rows, 24)
    except OSError:
        return 80, 24

