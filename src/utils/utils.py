import shutil
from typing import Tuple


def get_terminal_size() -> Tuple[int, int]:
    """
    Safely get terminal size, capped at (80, 24).
    """
    try:
        columns, rows = shutil.get_terminal_size()
        return min(columns, 80), min(rows, 24)
    except OSError:
        return 80, 24