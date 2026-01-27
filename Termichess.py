import chess
import os
import time

UNICODE_PIECES = {
    'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
    'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♙'
}

YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def start_of_game():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃      WELCOME TO  T E R M I C H E S S     ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    time.sleep(1)
    print("A two-player chess game in your terminal.")
    time.sleep(1)
    print("How to play:")
    time.sleep(1)
    print("  • Enter moves using SAN notation (e.g., e4, Nf3, Qxe7)")
    time.sleep(1)
    print("  • White moves first")
    time.sleep(1)
    print("  • Type 'quit' to exit the game")
    time.sleep(1)
    print("Battle is starting in")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Let the battle begin!")
    print("=============================================")
    time.sleep(1)

def help():
    print("\n=== CHESS ALGEBRAIC NOTATION (SAN) RULES ===\n")

    print("1. Basics:")
    print("   - Pieces: ♔ = King, ♕ = Queen, ♖ = Rook, ♗ = Bishop, ♘ = Knight, ♙ = Pawn")
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
    print("   - 'e.p.' some    times used for en passant (optional in many systems).")
    print("   - SAN always describes the move relative to the current board state.\n")

    print("=== END OF SAN RULES ===\n")


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw_board(board):
    print("┏━━━━━━━━━" + "┳━━━━━━━━━"*7 + "┓")
    for rank in range(7, -1, -1):
        for row in range(3):
            print("┃", end="")
            for file in range(8):
                sq = chess.square(file, rank)
                piece = board.piece_at(sq)

                if row == 1 and piece:
                    sym = UNICODE_PIECES[piece.symbol()]
                    color = YELLOW if piece.color == chess.WHITE else RED
                    print(f"{color}    {sym}    {RESET}┃", end="")
                else:
                    print("         ┃", end="")

            # print rank number on the middle row
            if row == 1:
                print(f" {rank+1}")
            else:
                print()
        if rank != 0:
            print("┣━━━━━━━━━" + "╋━━━━━━━━━"*7 + "┫")
    print("┗━━━━━━━━━" + "┻━━━━━━━━━"*7 + "┛")
    print("     a         b         c         d         e         f         g         h")

board = chess.Board()
history = []
clear()
start_of_game()

while True:
    clear()
    draw_board(board)

    print("\nMove history:")
    for i in range(0, len(history), 2):
        w = history[i]
        b = history[i+1] if i+1 < len(history) else ""
        print(f"{i//2+1}. {w} {b}")

    if board.is_checkmate():
        print("\nCHECKMATE!")
        print("Winner:", "Black" if board.turn else "White")
        break

    if board.is_stalemate():
        print("\nSTALEMATE! Draw.")
        break

    if board.is_insufficient_material():
        print("\nDraw: Insufficient material.")
        break

    if board.is_check():
        print("\nCHECK!")

    print("\nTurn:", "White" if board.turn else "Black")
    move_input = input("Enter move (e4, Nf3, O-O, e2e4) or q(to quit) or h(to help): ").strip()

    if move_input.lower() == "q":
        break

    if move_input.lower() == "h":
        clear()
        help()
        input("Press Enter to continue game\n")
        continue
    try:
        move = board.parse_san(move_input)
    except:
        try:
            move = chess.Move.from_uci(move_input)
        except:
            input("Invalid move format! Press Enter...")
            continue

    if move in board.legal_moves:
        history.append(board.san(move))
        board.push(move)
    else:
        input("Illegal move! Press Enter...")