import chess
from typing import Optional

"""
ascii chess charchters
'♔'	
'♕'
'♖'
'♗'
'♘'	
'♙'	
'♚'	
'♛'	
'♜'	
'♝'	
'♞'	
'♟' 
"""


# ---------------------------------------------------------
# STYLE 1: SOLID BOX-DRAW GRID (no ANSI colors)
# ---------------------------------------------------------
def print_solid_board(board: chess.Board, flipped: bool = False) -> None:
    files: str = 'A  B C D E F  G H'
    ranks = range(8, 0, -1)
    if flipped:
        files = files[::-1]
        ranks = range(1, 9)

    print("\n        " + "   ".join(files))
    print("     " + "┏━━━━━━━━" + "┳━━━━━━━━" * 7 + "┓")

    for row in range(8):
        rank = 8 - row

        # Empty padding row
        print("     " + "┃        " * 8 + "┃")

        # Row with pieces
        print(f"  {rank}  ", end="")
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            content = piece.symbol() if piece else " "
            print(f"┃   {content:^3}  ", end="")
        print("┃")

        # Empty padding row
        print("     " + "┃        " * 8 + "┃")

        if row < 7:
            print("     " + "┣━━━━━━━━" + "╋━━━━━━━━" * 7 + "┫")

    print("     " + "┗━━━━━━━━" + "┻━━━━━━━━" * 7 + "┛")
    print()
    print(f"\nTurn: {'White' if board.turn else 'Black'}")
    print("Enter move (e.g., e4, Nf3 or 'quit':")


# ---------------------------------------------------------
# STYLE 2: SIMPLE ANSI COLORED BOARD
# ---------------------------------------------------------
def print_simple_board(board: chess.Board, term_width: int = 80) -> None:
    print("\n" + "=" * term_width + "\n")

    square_width = max(1, (term_width - 12) // 8)

    dark_bg = "\033[48;2;60;60;60m\033[97m"
    light_bg = "\033[48;2;220;180;130m\033[30m"
    reset = "\033[0m"

    # File labels
    print("  ", end="")
    for col in range(8):
        print(f"{chr(97 + col):^{square_width}}", end="")
    print()

    # Board rows
    for row in range(8):
        print(f"{8 - row:>2} ", end="")
        for col in range(8):
            piece: Optional[chess.Piece] = board.piece_at(chess.square(col, 7 - row))
            bg = dark_bg if (row + col) % 2 == 0 else light_bg
            content = piece.symbol() if piece else " "
            print(f"{bg}{content:^{square_width}}{reset}", end="")
        print(f" {8 - row}")

    # File labels bottom
    print("  ", end="")
    for col in range(8):
        print(f"{chr(97 + col):^{square_width}}", end="")
    print()

    print(f"\nTurn: {'White' if board.turn else 'Black'}")
    print("Enter move (e.g., e4, Nf3 or 'quit':")


# ---------------------------------------------------------
# STYLE DISPATCHER
# ---------------------------------------------------------
def print_board(board: chess.Board, style="simple", term_width=80) -> None:
    """
    Dispatch to the correct board style.
    Accepts any type for style; converts safely to string.
    """
    style = str(style).lower()

    if style in ["solid", "0"]:
        print_solid_board(board)

    elif style in ["simple", "1"]:
        print_simple_board(board, term_width)

    else:
        print(f"Unknown board style '{style}', defaulting to simple.")
        print_simple_board(board, term_width)