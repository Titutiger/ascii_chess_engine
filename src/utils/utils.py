# This is a file to parce input strings from the user(s):

#imports:
import shutil
import chess
from typing import Tuple


def get_terminal_size() -> Tuple[int, int]:
    """
    Get the current terminal dimensions.

    Retrieves the terminal width (columns) and height (rows) using
    shutil.get_terminal_size(). Returns capped values for reasonable display.

    Parameters
    ----------
    None

    Returns
    -------
    Tuple[int, int]
        (columns, rows) of terminal size, capped at (80, 24)

    Raises
    ------
    OSError
        If terminal size cannot be determined
    """
    try:
        columns, rows = shutil.get_terminal_size()
        return min(columns, 80), min(rows, 24)
    except OSError:
        return 80, 24
