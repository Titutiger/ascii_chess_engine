import chess
from typing import Optional

from utils import get_terminal_size
from board import print_board
import sys

def main(style: str = "simple") -> None:
    """
    Main game loop for 2-player terminal chess.
    """
    board = chess.Board()

    while not board.is_game_over():
        term_width, _ = get_terminal_size()

        print_board(board, style=style, term_width=term_width)

        try:
            move_str = input("> ").strip() #.lower()

            if move_str in ["q", "quit", "esc"]:
                return

            # Validate move: try UCI first, then SAN
            legal_move: Optional[chess.Move] = None
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    legal_move = move
            except ValueError:
                # Try SAN
                for legal in board.legal_moves:
                    if board.san(legal) == move_str:
                        legal_move = legal
                        break

            if legal_move:
                board.push(legal_move)
                print(f"\n✓ Legal move: {board.san(legal_move)}")
            else:
                print(f"\n✗ Illegal move: {move_str}")

        except KeyboardInterrupt:
            print("\nGoodbye")
            return

    # Game over
    term_width, _ = get_terminal_size()
    print_board(board, style=style, term_width=term_width)
    print(f"\nGame over: {board.result()}")


if __name__ == "__main__":
    style = sys.argv[1] if len(sys.argv) > 1 else "simple"
    main(style=style)