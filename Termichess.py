import chess
import os
import time

# ================= CONSTANTS =================

UNICODE_PIECES = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♙'
}

YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# ================= UTILS =================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================= UI =====================

def start_of_game(t: int = 1):
    banner = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃      WELCOME TO  T E R M I C H E S S     ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    print(banner)
    time.sleep(t)
    print("A two-player chess game in your terminal.")
    time.sleep(t)
    print("How to play:")
    time.sleep(t)
    print("  • Enter moves using SAN notation (e.g., e4, Nf3, Qxe7)")
    time.sleep(t)
    print("  • White moves first")
    time.sleep(t)
    print("  • Type 'quit' to exit the game")
    time.sleep(t+2)
    print("Battle is starting in")
    print("3")
    time.sleep(t)
    print("2")
    time.sleep(t)
    print("1")
    time.sleep(t)
    print("Let the battle begin!")
    print("=============================================")
    time.sleep(t)

# ================= HELPS =====================

def command_menu():
    print("\n=== COMMAND MENU ===\n")

    print("Move Input:")
    print("  e4, Nf3, Qxe7, O-O, e2e4")

    print("\nCommands:")
    print("  q   → Quit game")
    print("  u   → Undo last move")
    print("  l   → Show all legal moves")
    print("  h   → Show SAN notation help")
    print("  hh  → Show this command menu")

    print("\nPiece Help Commands:")
    print("  hP  → Pawn help")
    print("  hN  → Knight help")
    print("  hB  → Bishop help")
    print("  hR  → Rook help")
    print("  hQ  → Queen help")
    print("  hK  → King help")

    print("\n====================\n")


def piece_help(piece):
    piece = piece.upper()

    print("\n=== PIECE HELP ===\n")

    if piece == "P":
        print("Pawn (P):")
        print("- Moves forward 1 square")
        print("- Captures diagonally")
        print("- Can move 2 squares from starting position")
        print("- Promotes on last rank (e8 or e1)")
        print("- Can capture en passant")

    elif piece == "N":
        print("Knight (N):")
        print("- Moves in an L-shape: 2 squares + 1 square")
        print("- Can jump over other pieces")

    elif piece == "B":
        print("Bishop (B):")
        print("- Moves diagonally any number of squares")

    elif piece == "R":
        print("Rook (R):")
        print("- Moves horizontally or vertically any number of squares")
        print("- Used in castling")

    elif piece == "Q":
        print("Queen (Q):")
        print("- Moves like a rook + bishop combined")
        print("- Any number of squares in any direction")

    elif piece == "K":
        print("King (K):")
        print("- Moves 1 square in any direction")
        print("- Special move: castling (O-O or O-O-O)")
        print("- Cannot move into check")

    else:
        print("Unknown piece type!")
        print("Use: hP, hN, hB, hR, hQ, hK")

    print("\n==================\n")

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

def get_legal_moves(board: chess.Board, piece_char: str | None = None) -> list[str]:
    """Returns a list of legal moves for that specific piece type"""
    piece_map = { # associates `p` -> chess.PAWN, etc...
        "p": chess.PAWN,
        "n": chess.KNIGHT,
        "b": chess.BISHOP,
        "r": chess.ROOK,
        "q": chess.QUEEN,
        "k": chess.KING,
    }

    # No piece → all moves (REDUNDANT)
    #if piece_char is None:
    #    return [board.san(m) for m in board.legal_moves]

    pc = piece_char.lower()
    if pc not in piece_map:
        return [] # returns none if the string holds a letter which is not
                  # a chess piece.

    pt = piece_map[pc] # converts `p` -> chess.PAWN

    return [
        board.san(m) # returns SAN for piece move
        for m in board.legal_moves # for all legal moves
        if board.piece_at(m.from_square) # checks what is moving and where
        and board.piece_at(m.from_square).piece_type == pt # checks the piece is in pt
    ]



def end_of_game():
    clear()
    draw_board(board, True)
    print("\nFinal Move history:")
    for i in range(0, len(history), 2):
        w = history[i]
        b = history[i+1] if i+1 < len(history) else ""
        print(f"{i//2+1}. {w} {b}")

def draw_board(board, end=False):
    if end:
        flip = False
    else:
        flip = not board.turn

    ranks = range(7, -1, -1) if not flip else range(8)
    files = range(8) if not flip else range(7, -1, -1)

    print("┏━━━━━━━━━" + "┳━━━━━━━━━"*7 + "┓")

    for rank in ranks:
        for row in range(3):
            print("┃", end="")
            for file in files:
                sq = chess.square(file, rank)
                piece = board.piece_at(sq)

                if row == 1 and piece:
                    sym = UNICODE_PIECES[piece.symbol()]
                    color = YELLOW if piece.color == chess.WHITE else RED
                    print(f"{color}    {sym}    {RESET}┃", end="")
                else:
                    print("         ┃", end="")

            if row == 1:
                print(f" {rank+1}")
            else:
                print()

        if rank != (0 if not flip else 7):
            print("┣━━━━━━━━━" + "╋━━━━━━━━━"*7 + "┫")

    print("┗━━━━━━━━━" + "┻━━━━━━━━━"*7 + "┛")

    files_label = ["a","b","c","d","e","f","g","h"]
    if flip:
        files_label.reverse()

    print("  " + "".join(f"   {f}      " for f in files_label))


def game_over():
    if board.is_checkmate():
        end_of_game()
        print("\nCHECKMATE!")
        print("Winner:", "Black" if board.turn == chess.WHITE else "White")
        return True

    if board.is_stalemate():
        end_of_game()
        print("\nSTALEMATE! Draw.")
        return True

    if board.is_insufficient_material():
        end_of_game()
        print("\nDraw: Insufficient material.")
        return True

    if board.can_claim_threefold_repetition():
        end_of_game()
        print("\nDraw: Threefold repetition.")
        return True

    if board.can_claim_fifty_moves():
        end_of_game()
        print("\nDraw: 50-move rule.")
        return True

    return False

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

    if game_over():
        break

    if board.is_check():
        print("\nCHECK!")

    print("\nTurn:", "White" if board.turn else "Black")
    move_input = input(
        "Enter move | u(undo) q(quit) l(legal) h(help) hh(menu): "
    ).strip()

    # handles quitting before move parsing because errors can be made.
    if move_input in ['q', 'quit', 'esc']:
        break

    # parses the move
    if move_input and move_input[0] in "pnbrqk":
        move_input = move_input[0].upper() + move_input[1:]


    if move_input == "u":
        if len(board.move_stack) > 0 and len(history) > 0:
            board.pop() # neat
            history.pop()
        else:
            input("No moves to undo! Press Enter...")
        continue

    if move_input == 'l': # let's list of all legal moves for all pieces
        for i, move in enumerate(board.legal_moves):
            print(f"{i}.", board.san(move))
        input("Press Enter to continue game\n")
        continue

    # ---- HELP SYSTEM ----

    if move_input == "hh":
        clear()
        command_menu()
        input("Press Enter to continue...\n")
        continue

    if move_input == "h":
        clear()
        help()
        input('Press enter to continue the game\n')
        continue

    if move_input.startswith("h") and len(move_input) == 2:
        piece = move_input[1].upper()
        if piece in "PNBRK":
            clear()
            piece_help(piece)
            print("\nLegal moves:")
            moves = get_legal_moves(board, piece)
            if moves:
                print(", ".join(moves))
            else:
                print("No legal moves.")
            input("Press Enter...")
        else:
            print("Use: hP hN hB hR hQ hK")
            input("Press Enter...")
        continue

    try:
        move = board.parse_san(move_input)
    except ValueError:
        print("Illegal move!")
        continue

    history.append(board.san(move))
    board.push(move)
