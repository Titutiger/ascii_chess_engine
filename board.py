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
