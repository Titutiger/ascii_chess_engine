# Rules.py

import src.utils as utils

"""
This file dictates the legal moves present,
checkmates, stalemates and drawing conditions.

It also contains special moves.
"""

def is_legal(move: str) -> bool:
    """
    Checks if a move made is legal or not in the form of a bool.
    Here, move is a string which is in ACN.
    The function will call the parser to convert ACN to FEN.
    The FEN will be evalutated, on which, a boolean will be returned.

    Parameters:
    -----------
    move: str
        Move to be checked.

    Returns:
    --------
        is_legal: bool

    Raises:
    -------
    ...

    Examples:
    ---------
    >>> is_legal('QxE4')
    """
    ...
