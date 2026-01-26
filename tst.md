# TermiChess
#### Video Demo: <https://drive.google.com/file/d/186m1l3tpF0DdniCpr88x13E3xfZy0fDg/view?usp=sharing>

###### Project by Aarin J (GitHub: Titutiger)

#### Description:
TermiChess is terminal-based chess written in Python. The
program uses the python-chess library to validate moves.
This project focuses on minimalist style terminal programs.

___

#### Detail:
This project uses the `python-chess` library to handle
chess rules and legality checks.

This project compartmentalizes functions based on logic,
UI and the main game loop.

##### Helpers:

`normalize_input()` helps in restructuring castling and
properly formatting pawn promotions.

`board_to_string()` provides a pretty matrix of a chess
board. Before using the implemented 'pretty' style, I
implemented a more pipelined approach (literally), with
using ASCII bars as borders for the board. However, I
found it to be too cluttered, therefore the current board:

```python
rows = []
for rank in range(8, 0, -1):
    row = []
    for file in range(8):
        piece = board.piece_at(chess.square(file, rank - 1))
        row.append(piece.symbol() if piece else ".")
    rows.append(" ".join(row))
return "\n".join(rows)
```

Since terminal programs are generally bare bones, this was
another reason to design the board in a minimalist sense,
wherein nothing is overpowering others, and the player can
focus on the main task, i.e, the game itself.

`get_legal_moves()` does exactly what it says, it gets a
list of legal moves which the active player can perform.

`is_move_legal()` is as straightforward as it gets, it
checks if the move is legal or not.

These functions act as reusable APIs for the game loop
as well as for future versions.
___

##### UI:

`print_board()` prints the board to the terminal and
displays which player is active.

`print_legal_moves()` calls `get_legal_moves()` to
display to the user.
Herein, I found the syntax for calling this function
to be quite clean from the user's POV.
```commandline
h <piece_type>
```
It allows the user to check legality by performing the
least number of keystrokes.

___

##### Loop:

`main()` is where the game loop rests. It calls on all
functions to execute the game sequentially. Here lies
the visible and playable input/output of the program.
In:

```python
try:
    move = chess.Move.from_uci(move_str.lower())
except ValueError:
    # SAN move fallback
    move = next(m for m in board.legal_moves if board.san(m) == move_str)

board.push(move)
```

Some may be familiar with UCI rather than SAN, therefore
the option to choose both.
___

#### Future:

- Add move history and an evaluation framework.
- Making an interactive version using TUI frameworks
such as Textual.
- Stockfish integration at selectable ELO ratings.
