# This is a file to parce input strings from the user(s):

def parse(string: str, type_: str = 'parse', ) -> str:
    """
    This function parses a string and returns it as a string.
    If `type_` is ACN, then this function will return FEN and vice versa.

    Parameters:
    -----------
    string: str
        The string to parse.
    type_: str
        The type to parse; This includes:
        `parse`,
        `ACN` This stands for Algebraic Chess Notation,
        `FEN` Forsyth-Edwards Notation,

    Returns:
    --------
    string: str

    Raises:
    -------
    ...

    :return:
    """
    if type_ == 'parse':
        if string == "":
            ...

    elif type_ == 'ACN':
        ...
    # return FEN

    elif type_ == 'FEN':
        ...
    # return ACN

