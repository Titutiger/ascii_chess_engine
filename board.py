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

def board(style: str = 'solid') -> str:
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

    elif style == 'pipe':
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

if __name__ == '__main__':
    board(style='pipe')
    board()