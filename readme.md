# TermiChess
###### ~ Python
___
~ Aarin J and Ojas K

___

### Project details and execution:
```python
python_environment: float =  3.12

libraries_used: dict = {
    'textual': 'terminal based user interface',
    'rich': 'colors',
    'python-chess': 'library for handling game logic'
}
```
##### Execution:
Download the .zip from
<a href='https://github.com/Titutiger/ascii_chess_engine'>github</a> and extracted.
Provided that python is installed, remember to execute:

Firstly, go into the virtual environment via making one.
On VS CODE, select the python version at the bottom right, and then select `create virtual environment`.
Then, it will take some time and after that, your virtual environment is set up.

The terminal prompt should start with `(.venv)`. If it doesn't, then execute every
statement with this:
```commandline
.venv\Scripts\python ...
```
```commandline
python -m pip install -r requirements.txt
```
And once that is done, do execute:
```commandline
python distributable/dashboard-tex.py

OR
.venv\Scripts\python distributable/dashboard-tex.py
```


IF THE NORMAL `board_tex.py` doesn't work, then use:

```commandline
python distributable/board_tex_ascii.py
```

___

### Features:


___

File structure:
```
repo/
  main.py (DEPRECATED) (EMPTY)
  requirements.txt
  readme.md
  temp.py (DEPRECATED) (NOT IN USE)
  
  venv/
    ...
  distributable/
    board.py
    board_tex.py
    dashboard-tex.py
    game.py
    main.py (DEPRECATED) (REPLACED WITH dashboard-tex.py)
    utils.py
  test/
    demo.py
    layouttest.py
  
```

### Program:

Program execution starts with `python distributalbe/dashboard-tex.py`,
this loads the TUI (Terminal User Interface) onto the terminal.

The start screen showcases a label asking the user for the game mode.
2 drop-down options are given: Choose interface and Choose game mode.

In Choose interface, there are: 
1. TUI (Graphical)
2. CMD (Text Based)

And in Choose game mode, there are:
1. against player (local)
2. against machine (stockfish) ###DEPRICATED###

If the user chooses TUI, then `board_tex.py` will execute.
If the user chooses CMD, then `game.py` will execute. In CMD, the user also
has a choice of the theme of the board.

The logic of moves is handled by the respective programs (TUI, CMD).