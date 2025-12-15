import chess
from typing import Optional

from utils import get_terminal_size
from board import print_board


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

            # Validate move by comparing SAN strings
            legal_move: Optional[chess.Move] = None
            for legal in board.legal_moves:
                if board.san(legal) == move_str:
                    legal_move = legal
                    break

            if legal_move:
                board.push(legal_move)
                print(f"\n✓ Legal move: {move_str}")
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
    print("Terminal Chess — 2 Player (Auto-scaling)")
    print('Enter `n` for UCI notation or `h` for help.')

    q = str(input("Press Enter to start: "))
    if q in ['n']:
        print("\n=== CHESS ALGEBRAIC NOTATION (SAN) RULES ===\n")

        print("1. Basics:")
        print("   - Pieces: K = King, Q = Queen, R = Rook, B = Bishop, N = Knight")
        print("   - Pawns have no letter (just the destination square).")
        print("   - Squares are file + rank, e.g., e4, a1, h8.\n")

        print("2. Simple moves:")
        print("   - Pawn move: e4   (pawn goes to e4)")
        print("   - Piece move: Nf3 (knight goes to f3)")
        print("   - No starting square in basic SAN; it's inferred from the position.\n")

        print("3. Captures:")
        print("   - Pawn capture: exd5  (pawn from e-file captures on d5)")
        print("   - Piece capture: Qxe6 (queen captures on e6)")
        print("   - 'x' indicates a capture.\n")

        print("4. Promotions:")
        print("   - Pawn promotes when reaching last rank:")
        print("   - e8=Q  (pawn moves to e8 and becomes a queen)")
        print("   - exd8=N (pawn from e-file captures on d8 and becomes a knight)\n")

        print("5. Castling:")
        print("   - Kingside:  O-O")
        print("   - Queenside: O-O-O\n")

        print("6. Check and checkmate:")
        print("   - '+' added for check:     Qh5+")
        print("   - '#' added for checkmate: Qh7#")
        print("   - Can combine with captures: Rxe8+ or Qxh7#\n")

        print("7. Disambiguation (when two same pieces can move to same square):")
        print("   - Add file, rank, or both of the starting square:")
        print("   - Nbd2 (knight from b-file goes to d2)")
        print("   - N1f3 (knight from rank 1 goes to f3)")
        print("   - Qh4e1 (queen from h4 goes to e1) — rare but legal SAN.\n")

        print("8. Specials:")
        print("   - 'x' omitted if not a capture.")
        print("   - 'e.p.' sometimes used for en passant (optional in many systems).")
        print("   - SAN always describes the move relative to the current board state.\n")

        print("=== END OF SAN RULES ===\n")

    else:
        main(style="simple")   # Change to "simple" or "solid"