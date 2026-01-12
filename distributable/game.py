import chess
from typing import Optional

from utils import get_terminal_size, Colors
from board import print_board
import sys


def normalize_input(move_str: str) -> str:
    """Normalize common user input quirks without breaking SAN."""
    s = move_str.strip()

    # Castling variants
    if s.lower() in ("o-o", "0-0"):
        return "O-O"
    if s.lower() in ("o-o-o", "0-0-0"):
        return "O-O-O"

    # Promotion shorthand: e8q -> e8=Q
    if len(s) == 3 and s[2].lower() in "qrbn":
        return s[:2] + "=" + s[2].upper()

    return s


def list_legal_moves_by_piece(board: chess.Board, piece_char: str) -> None:
    piece_map = {
        "p": chess.PAWN,
        "n": chess.KNIGHT,
        "b": chess.BISHOP,
        "r": chess.ROOK,
        "q": chess.QUEEN,
        "k": chess.KING,
    }

    piece_char = piece_char.lower()
    if piece_char not in piece_map:
        print("Unknown piece. Use p n b r q k")
        return

    piece_type = piece_map[piece_char]

    moves = [
        board.san(move)
        for move in board.legal_moves
        if board.piece_at(move.from_square)
        and board.piece_at(move.from_square).piece_type == piece_type
    ]

    piece_name = chess.piece_name(piece_type).capitalize()

    if moves:
        print(f"\nLegal {piece_name} moves:")
        for m in moves:
            print(f'{Colors.INFO}{m}{Colors.RESET}')
    else:
        print(f"\n{Colors.ERROR}No legal {piece_name} moves available.{Colors.RESET}")


def main(style: str = "simple") -> None:
    board = chess.Board()

    while not board.is_game_over():
        term_width, _ = get_terminal_size()
        print_board(board, style=style, term_width=term_width)

        try:
            raw_input = input("> ").strip()

            # Quit (case-insensitive)
            if raw_input.lower() in ("q", "quit", "esc"):
                print(f'{Colors.WARNING}Are you sure you want to surrender?{Colors.RESET}')
                if input(">>> ").lower() in ("y", "yes"):
                    return
                else: continue

            # Help command
            if raw_input.lower().startswith("h "):
                _, piece_char = raw_input.split(maxsplit=1)
                list_legal_moves_by_piece(board, piece_char)
                continue

            move_str = normalize_input(raw_input)

            legal_move: Optional[chess.Move] = None

            # 1️⃣ Try UCI
            try:
                move = chess.Move.from_uci(move_str.lower())
                if move in board.legal_moves:
                    legal_move = move
            except ValueError:
                pass

            # 2️⃣ Try SAN (exact, case-sensitive)
            if not legal_move:
                san_matches = [
                    legal
                    for legal in board.legal_moves
                    if board.san(legal) == move_str
                ]

                if len(san_matches) == 1:
                    legal_move = san_matches[0]

                elif len(san_matches) > 1:
                    print("\nAmbiguous move. Possible moves:")
                    for m in san_matches:
                        print(board.san(m))
                    continue

            if legal_move:
                san = board.san(legal_move)
                board.push(legal_move)
                print(f"\n{Colors.SUCCESS}✓ Legal move: {san}{Colors.RESET}")
            else:
                print(f"\n{Colors.ERROR}✗ Illegal move: {raw_input}{Colors.RESET}")

        except KeyboardInterrupt:
            print("\nGoodbye")
            return

    # Game over
    term_width, _ = get_terminal_size()
    print_board(board, style=style, term_width=term_width)

    if board.is_checkmate():
        print("\nCheckmate!")
    elif board.is_stalemate():
        print("\nStalemate.")
    elif board.is_insufficient_material():
        print("\nDraw: insufficient material.")
    else:
        print(f"\nGame over: {board.result()}")


if __name__ == "__main__":
    style = sys.argv[1] if len(sys.argv) > 1 else "simple"
    main(style=style)
