from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Select, Button, Input
from textual.containers import Vertical, Horizontal, Center, ScrollableContainer
from textual.screen import Screen
from textual import events
import time
import subprocess
import sys
import os

from game import main as execute
from utils import run_in_new_cmd




class TermiChess(App):
    CSS = """
    Screen {
        layout: vertical;
        align: center middle;
    }

    #welcome {
        text-align: center;
        margin-bottom: 2;
        color: green;
    }

    #subtitle {
        text-align: center;
        margin-bottom: 3;
        color: white;
    }

    #interface-select {
        width: 40;
        margin-bottom: 2;
    }

    #mode-select {
        width: 40;
        margin-bottom: 2;
    }

    #interface-container{
        margin-bottom: 2;
    }

    #style-container{
        display: none;
        margin-bottom: 2;
    }
    
    #style-select {
        width: 40;
    }

    #submit-button {
        margin-top: 2;
    }
    #help {
        margin-top: 2;
    }
    ScrollableContainer {
        scrollbar-size-vertical: 3;
        
        scrollbar-background: transparent;
        scrollbar-gutter: stable;
    }
    """
    #theme = 'light'

    def __init__(self):
        super().__init__()
        self.selected_mode = None
        self.difficulty_level = None
        self.selected_style = "simple"
        self.interface_value = None

    class HelpScreen(Screen):
        def compose(self) -> ComposeResult:
            yield Header()
            with Center():
                with ScrollableContainer():
                    with Vertical():
                        with Center():
                            yield Static('CHESS ALGEBRAIC NOTATION (SAN) RULES', id='help-title')
                        with ScrollableContainer():
                            yield Static('')
                            yield Static('1. Basics:')
                            yield Static('   - Pieces: K = King, Q = Queen, R = Rook, B = Bishop, N = Knight')
                            yield Static('   - Pawns have no letter (just the destination square).')
                            yield Static('   - Squares are file + rank, e.g., e4, a1, h8.')
                            yield Static('')
                            yield Static('2. Simple moves:')
                            yield Static('   - Pawn move: e4   (pawn goes to e4)')
                            yield Static('   - Piece move: Nf3 (knight goes to f3)')
                            yield Static('   - No starting square in basic SAN; it\'s inferred from the position.')
                            yield Static('')
                            yield Static('3. Captures:')
                            yield Static('   - Pawn capture: exd5  (pawn from e-file captures on d5)')
                            yield Static('   - Piece capture: Qxe6 (queen captures on e6)')
                            yield Static('   - \'x\' indicates a capture.')
                            yield Static('')
                            yield Static('4. Promotions:')
                            yield Static('   - Pawn promotes when reaching last rank:')
                            yield Static('   - e8=Q  (pawn moves to e8 and becomes a queen)')
                            yield Static('   - exd8=N (pawn from e-file captures on d8 and becomes a knight)')
                            yield Static('')
                            yield Static('5. Castling:')
                            yield Static('   - Kingside:  O-O')
                            yield Static('   - Queenside: O-O-O')
                            yield Static('')
                            yield Static('6. Check and checkmate:')
                            yield Static('   - \'+\' added for check:     Qh5+')
                            yield Static('   - \'#\' added for checkmate: Qh7#')
                            yield Static('   - Can combine with captures: Rxe8+ or Qxh7#')
                            yield Static('')
                            yield Static('7. Disambiguation (when two same pieces can move to same square):')
                            yield Static('   - Add file, rank, or both of the starting square:')
                            yield Static('   - Nbd2 (knight from b-file goes to d2)')
                            yield Static('   - N1f3 (knight from rank 1 goes to f3)')
                            yield Static('   - Qh4e1 (queen from h4 goes to e1) — rare but legal SAN.')
                            yield Static('')
                            yield Static('8. Specials:')
                            yield Static('   - \'x\' omitted if not a capture.')
                            yield Static('   - \'e.p.\' sometimes used for en passant (optional in many systems).')
                            yield Static('   - SAN always describes the move relative to the current board state.')
                            yield Static('')
                            with Center():
                                yield Button('Back', id='back-button')

        def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == 'back-button':
                self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical():
                with Center():
                    yield Static("Welcome to TermiChess!", id="welcome")
                with Center():
                    yield Static("Please select which mode you wish to play:", id="subtitle")

                with Center():
                    yield Select(
                        [('TUI (Graphical)', 'ui'), ('CMD (Text Based)', 'text')],
                        prompt='Choose interface...',
                        id='interface-select'
                    )

                with Center():
                    yield Select(
                        [("against player (local)", "local"), ("against machine (stockfish)", "stockfish")],
                        prompt="Choose game mode...",
                        id="mode-select"
                    )

                with Vertical(id="style-container"):
                    with Center():
                        yield Select(
                            # display    style      display   style
                            [('solid', '0'), ('colour', '1')],
                            prompt='Choose style...',
                            id="style-select"
                        )

        yield Footer()
        with Center():
            yield Button('Help?', id='help')
            yield Button("Start Game", id="submit-button")

    def on_select_changed(self, event: Select.Changed) -> None:
        # Interface selection (THIS controls style visibility)
        if event.select.id == "interface-select":
            style_container = self.query_one("#style-container")

            if event.value == "text":  # CMD
                style_container.display = True
                self.interface_value = 'text'
            else:  # ui
                style_container.display = False
                self.interface_value = 'ui'

        # Game mode selection
        elif event.select.id == "mode-select":
            self.selected_mode = event.value

        # Style selection
        elif event.select.id == "style-select":
            self.selected_style = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'help':
            self.push_screen(self.HelpScreen())

        elif event.button.id == "submit-button":
            if self.selected_mode == "local":
                self.notify("Starting local game against another player!") # Cool feature!
                time.sleep(4)
                #self.exit()
                if self.interface_value == 'text':
                    #os.system(f'start cmd /k python game.py {self.selected_style}')
                    run_in_new_cmd('game.py', self.selected_style)

                else:
                    #os.system(f'start cmd /k python board_tex.py')
                    run_in_new_cmd('board_tex.py')


            elif self.selected_mode == "stockfish":
                if self.difficulty_level:
                    self.notify(f"Starting game against Stockfish at ELO {self.difficulty_level}!")
                    # Here you would start the stockfish game with the selected difficulty
                else:
                    self.notify("Please select a difficulty level for Stockfish.", severity="error")
            else:
                self.notify("Please select a game mode.", severity="error")

if __name__ == "__main__":
    app = TermiChess()
    app.run()
