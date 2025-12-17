import shutil
from typing import Tuple

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