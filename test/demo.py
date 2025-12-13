import chess
import os
import shutil
from typing import Tuple, Optional


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

def print_board(board: chess.Board, term_width: int = 80, term_height: int = 24) -> None:
    """
    Print a formatted, scaled chessboard to terminal.

    Displays the chessboard with alternating colored squares, piece symbols,
    rank/file labels, and current turn information. Scales dynamically based
    on terminal dimensions.

    Parameters
    ----------
    board : chess.Board
        The current chess board state
    term_width : int, optional
        Terminal width in columns (default: 80)
    term_height : int, optional
        Terminal height in rows (default: 24)

    Returns
    -------
    None
    """

    print("\n" + "=" * term_width + "\n")  # Visual separator instead

    square_width: int = max(1, (term_width - 12) // 8)

    '''
    clear_screen()
    square_width: int = max(1, (term_width - 12) // 8)
    '''

    dark_bg: str = "\033[48;2;60;60;60m\033[97m"
    light_bg: str = "\033[48;2;220;180;130m\033[30m"
    reset: str = "\033[0m"

    print(f"  ", end="")
    for col in range(8):
        print(f"{chr(97 + col):^{square_width}}", end="")
    print()

    for row in range(8):
        print(f"{8 - row:>2} ", end="")
        for col in range(8):
            piece: Optional[chess.Piece] = board.piece_at(chess.square(col, 7 - row))
            bg: str = dark_bg if (row + col) % 2 == 0 else light_bg
            content: str = piece.symbol() if piece else " "
            print(f"{bg}{content:^{square_width}}{reset}", end="")
        print(f" {8 - row}")

    print("  ", end="")
    for col in range(8):
        print(f"{chr(97 + col):^{square_width}}", end="")
    print()

    print(f"\nTurn: {'White' if board.turn else 'Black'}")
    print("Enter move in ACN (e.g., 'e4', 'Nf3') or 'quit':")

def main() -> None:
    """
    Main game loop for 2-player terminal chess.

    Handles move input, validation, board updates, and game over conditions.
    Uses nested loops to ensure only legal moves advance the game state.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    board: chess.Board = chess.Board()

    while not board.is_game_over():
        term_width: int
        term_height: int
        term_width, term_height = get_terminal_size()
        while True:
            print_board(board, term_width, term_height)

            try:
                move_str: str = input("> ").strip().lower()

                if move_str in ['q', 'quit', 'esc']:
                    return

                # Check if move is legal FIRST (prevents parse_san error)
                legal_move: Optional[chess.Move] = None
                for legal in board.legal_moves:
                    if board.san(legal) == move_str:
                        legal_move = legal
                        break

                if legal_move:
                    board.push(legal_move)
                    print(f"\n✓ Legal move: {move_str}")
                    break  # Valid move, proceed to next turn
                else:
                    print(f"\n✗ Illegal move: {move_str}")
                    #input("Press Enter to try again...")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                return

    term_width, term_height = get_terminal_size()
    print_board(board, term_width, term_height)
    if board.is_game_over():
        print(f"\nGame over: {board.result()}")

if __name__ == "__main__":
    print("Terminal Chess - 2 Player (Auto-scaling)")
    input("Press Enter to start...")
    main()
