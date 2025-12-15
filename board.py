# base grid layout(not including any variables)
"""
Characters for grid
┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼
╔ ╗ ╚ ╝ ═ ║ ╠ ╣ ╦ ╩ ╬
╒ ╓ ╕ ╖ ╘ ╙ ╛ ╜ ╞ ╟ ╡ ╢
╤ ╥ ╧ ╨ ╪ ╫
━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋
+ - |
Using these to form the grid
"""
#import os

#def clrscr():
#    os.system('cls')
#clrscr()

def board(style: str = 'solid') -> None:
    if style == 'solid':
        print("\n         A        B        C        D        E        F        G        H")
        print("     "+"┏━━━━━━━━"+"┳━━━━━━━━"*7+"┓")
        print("     "+"┃        "*8+"┃")
        print("  1  "+"┃        "*8+"┃")
        print("     "+"┃        "*8+"┃")
        i = 0
        while i < 7:
            print("     "+"┣━━━━━━━━" + "╋━━━━━━━━"*7+"┫")
            print("     "+"┃        "*8+"┃")
            print("  "+str(i+2)+"  "+"┃        "*8+"┃    ")
            print("     "+"┃        "*8+"┃")
            i += 1
        print("     "+"┗━━━━━━━━" + "┻━━━━━━━━"*7+"┛")

    elif style in ['p', 'pipe']:
        print("\n         A        B        C        D        E        F        G        H")
        print("     " + "╔════════" + "╔════════" * 7 + "┓")
        print("     " + "║        " * 8 + "║")
        print("  1  " + "║        " * 8 + "║")
        print("     " + "║        " * 8 + "║")
        i = 0
        while i < 7:
            print("     " + "╫════════" + "╬════════" * 7 + "┫")
            print("     " + "║        " * 8 + "║")
            print("  " + str(i + 2) + "  " + "║        " * 8 + "║    ")
            print("     " + "║        " * 8 + "║")
            i += 1
        print("     " + "╚════════" + "╨════════" * 7 + "┛")

    elif style in ['s', 'sim', 'simple']:
        def print_chessboard():
            board = [
                ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
                ['♟'] * 8, ['.'] * 8, ['.'] * 8, ['.'] * 8, ['.'] * 8,
                ['♙'] * 8,
                ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
            ]

            print("\n" + " " * 3 + "a  b  c  d  e  f  g  h")
            for row in range(8):
                line = f"{8 - row} "
                for col in range(8):
                    piece = board[row][col]
                    # ANSI colors: dark squares \033[48;2;60;60;60m, light \033[48;2;220;180;130m
                    if (row + col) % 2 == 0:
                        # Dark square
                        line += f"\033[48;2;60;60;60m\033[97m {piece} \033[0m"
                    else:
                        # Light square
                        line += f"\033[48;2;220;180;130m\033[30m {piece} \033[0m"
                print(line + f" {8 - row}")
            print("   " + "a  b  c  d  e  f  g  h" + "\n")

        print_chessboard()


if __name__ == '__main__':
    board(style='s')
