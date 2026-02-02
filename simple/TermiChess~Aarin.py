# Terminal Chess Game

import chess

# ---------------------------------------------------------

def normalize_input(move_str: str) -> str:
    """Normalize chess move input"""
    s = move_str.strip() # removes leading and trailing whitespaces

    # castling
    if s.lower() in ("o-o", "0-0"):
        return "O-O"
    if s.lower() in ("o-o-o", "0-0-0"):
        return "O-O-O"
    # easier notation for castling

    # promotions
    if len(s) == 3 and s[2].lower() in "qrbn":
        return s[:2] + "=" + s[2].upper()
        # simple notation for promotions

    return s


def get_legal_moves(board: chess.Board, piece_char: str) -> list:
    """Return SAN moves for a given piece type"""
    piece_map = {
        "p": chess.PAWN,
        "n": chess.KNIGHT,
        "b": chess.BISHOP,
        "r": chess.ROOK,
        "q": chess.QUEEN,
        "k": chess.KING,
    }

    pc = piece_char.lower()
    if pc not in piece_map:
        raise ValueError("Invalid piece")

    pt = piece_map[pc]

    return [
        board.san(m)
        for m in board.legal_moves
        if board.piece_at(m.from_square)
        and board.piece_at(m.from_square).piece_type == pt
    ]
    # gets all legal moves of that piece and returns them in a list


def is_move_legal(board: chess.Board, move_str: str) -> bool:
    """checking if a move is a legal move."""
    move_str = normalize_input(move_str)

    try:
        move = chess.Move.from_uci(move_str.lower())
        return move in board.legal_moves # bool value of true/false
    except ValueError:
        return any(board.san(m) == move_str for m in board.legal_moves) # uses hardened SAN

def board_to_string(board: chess.Board) -> str:
    """Pretty chess board"""
    rows = []
    for rank in range(8, 0, -1):
        row = []
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank - 1))
            row.append(piece.symbol() if piece else ".") # prints . if blank else piece letter
        rows.append(" ".join(row))
    return "\n".join(rows)

# ---------------------------------------------------------
# UI FUNCTIONS (PRINTING)


def print_board(board: chess.Board):
    print("\n" + board_to_string(board))
    print(f"\nTurn: {'White' if board.turn else 'Black'}") # comprehension for active player


def print_legal_moves(board: chess.Board, piece_char: str):
    try:
        moves = get_legal_moves(board, piece_char)
        if not moves:
            print("No legal moves.")
        else:
            print("Legal moves:")
            for m in moves:
                print(m)
    except ValueError:
        print("Invalid piece!")


# ---------------------------------------------------------
# GAME LOOP

def main():
    board = chess.Board()

    while not board.is_game_over():
        print_board(board)
        move_input = input("> ").strip()

        # game exit
        if move_input.lower() in ("q", "quit"):
            print("Goodbye!")
            return

        # help (> h <piece_type>)
        if move_input.lower().startswith("h "):
            _, piece = move_input.split(maxsplit=1)
            print_legal_moves(board, piece)
            continue

        # legal move?
        if not is_move_legal(board, move_input):
            print("Illegal move!")
            continue

        move_str = normalize_input(move_input)
        try:
            move = chess.Move.from_uci(move_str.lower())
        except ValueError:
            # SAN move fallback
            move = next(m for m in board.legal_moves if board.san(m) == move_str)

        board.push(move)

    # finisher
    print_board(board)

    # ending outcomes and reasons
    if board.is_checkmate():
        winner = "Black" if board.turn else "White"
        print(f"\nCheckmate! {winner} wins.")

    elif board.is_stalemate():
        print("\nStalemate! Draw.")

    elif board.is_insufficient_material():
        print("\nDraw due to insufficient material.")

    elif board.can_claim_threefold_repetition():
        print("\nDraw by threefold repetition.")

    elif board.can_claim_fifty_moves():
        print("\nDraw by 50-move rule.")

    print("Game Over:", board.result())


if __name__ == "__main__":
    main()