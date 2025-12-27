from game import main as execute
import pyfiglet
import time

import utils

# Example fonts: 'standard', 'banner', 'big', 'small', 'alligator', 'isometric3'
font_name = "standard"
text = "TermiChess"

ascii_art = pyfiglet.figlet_format(text, font=font_name)

time.sleep(1)
print('Welcome to:')
time.sleep(1)
print(ascii_art)

time.sleep(2)

""" Intro: """
print('~Aarin and Ojas')
print()
print()
time.sleep(1)
                                            # add SAN and start-end notation thing

print("Terminal Chess — 2 Player")
print('`n` ~ UCI Notation\n'
      '`h` ~ help\n'
      '`q` ~ quit\n'
      '`i` ~ info\n'
      '`c` ~ config\n'
      '` ` ~ start')

q = str(input(": "))
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

elif q in ['i', 'info', 'information', 'about', 'a']:
    for i in range(10):
        print()
    print('Info:')
    print(f'Title: {utils.title}')
    print(f'Version dev: {utils.v_dev}\nVersion usr: {utils.v_usr}')
    print(f'Author: {utils.authors}')
    print(f'License: {utils.lic}')
    print(f'Inception date: {utils.inception}')
    print(f'')
    print('Program flow:')
    print("""
        Program start stings
        Asks user for choice of program type.
        Runs that specific task.
            Prints the board via user style and accepts SAN inputs.
            Checks for checkmates and stalemates.
            Checks if the said SAN inputs are legal (valid).
            If yes,
                Pushes the moves to the board and prints new board.
            If no,
                Rejects the move and prompts the user again for a legal move.
            Runs in a loop until there is a winner or it is a draw.
    """)


elif q in ['c', 'config', 's', 'settings']:
    for i in range(10):
        print()
    print('Config:')
    print('1 ~ board themes\n'
          '')

elif q in ['h', 'help', '?']:
    for i in range(10):
        print()
    print('Help:')
    print('1 ~ board themes\n')

    q_h = int(input(": "))

elif q in ['q', 'esc', 'quit']:
    pass

else:
    execute(style="simple")   # Change to "simple" or "solid"