# This is a file to parce input strings from the user(s):

#imports:
import chess

def parse(string_: str, type_: str = 'parse', ) -> str | None:
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
        if string_ == "":
            ...

    elif type_ == 'ACN':
        board = chess.Board()
        move = string_
        board.push_san(move)
        return board.fen()
    # return FEN

    elif type_ == 'FEN':
        fen = string_
        board = chess.Board(fen)
    # return ACN

