# ===============================
# TermiChess — ALL IN ONE FILE
# ===============================

import os
import sys
import time
import shutil
from typing import Optional, Tuple

import chess
import colorama
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Select
from textual.containers import Grid, Horizontal, Vertical, Center, ScrollableContainer
from textual.screen import Screen

# =========================================================
# UTILS (formerly utils.py)
# =========================================================

colorama.init()
USE_COLOR = True

class Colors:
    INFO = colorama.Fore.YELLOW if USE_COLOR else ""
    SUCCESS = colorama.Fore.GREEN if USE_COLOR else ""
    ERROR = colorama.Fore.RED if USE_COLOR else ""
    WARNING = colorama.Fore.MAGENTA if USE_COLOR else ""
    RESET = colorama.Style.RESET_ALL if USE_COLOR else ""

def get_terminal_size() -> Tuple[int, int]:
    try:
        columns, rows = shutil.get_terminal_size()
        return min(columns, 80), min(rows, 24)
    except OSError:
        return 80, 24


# =========================================================
# CMD BOARD RENDERING (formerly board.py)
# =========================================================

def print_solid_board(board: chess.Board) -> None:
    files = "ABCDEFGH"
    print("\n    " + "   ".join(files))
    print("  ┏" + "━━━┳" * 7 + "━━━┓")

    for rank in range(8, 0, -1):
        print(f"{rank} ┃", end="")
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank - 1))
            char = piece.symbol() if piece else " "
            print(f" {char} ┃", end="")
        print(f" {rank}")

        if rank > 1:
            print("  ┣" + "━━━╋" * 7 + "━━━┫")

    print("  ┗" + "━━━┻" * 7 + "━━━┛")
    print("    " + "   ".join(files))
    print(f"\nTurn: {'White' if board.turn else 'Black'}")
    print("Enter move:")

def print_simple_board(board: chess.Board, term_width: int = 80) -> None:
    print("\n" + "=" * term_width)
    for rank in range(8, 0, -1):
        print(f"{rank} ", end="")
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank - 1))
            print(piece.symbol() if piece else ".", end=" ")
        print(f" {rank}")
    print("  a b c d e f g h")
    print(f"\nTurn: {'White' if board.turn else 'Black'}")

def print_board(board: chess.Board, style="simple", term_width=80) -> None:
    if style in ("solid", "0"):
        print_solid_board(board)
    else:
        print_simple_board(board, term_width)


# =========================================================
# CMD GAME LOOP (formerly game.py)
# =========================================================

def normalize_input(move_str: str) -> str:
    s = move_str.strip()
    if s.lower() in ("o-o", "0-0"):
        return "O-O"
    if s.lower() in ("o-o-o", "0-0-0"):
        return "O-O-O"
    if len(s) == 3 and s[2].lower() in "qrbn":
        return s[:2] + "=" + s[2].upper()
    return s

def run_cmd_game(style="simple"):
    board = chess.Board()

    while not board.is_game_over():
        w, _ = get_terminal_size()
        print_board(board, style, w)

        move_raw = input("> ").strip()
        if move_raw.lower() in ("q", "quit"):
            return

        move_str = normalize_input(move_raw)
        move = None

        try:
            candidate = chess.Move.from_uci(move_str.lower())
            if candidate in board.legal_moves:
                move = candidate
        except ValueError:
            pass

        if not move:
            for legal in board.legal_moves:
                if board.san(legal) == move_str:
                    move = legal
                    break

        if move:
            board.push(move)
            print(f"{Colors.SUCCESS}✓ Move played{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}✗ Illegal move{Colors.RESET}")

    print_board(board, style)
    print("Game over:", board.result())


# =========================================================
# TEXTUAL TUI CHESS (merged board_tex)
# =========================================================

WHITE_PIECES = {
    chess.PAWN: "♙", chess.ROOK: "♖", chess.KNIGHT: "♘",
    chess.BISHOP: "♗", chess.QUEEN: "♕", chess.KING: "♔",
}
BLACK_PIECES = {
    chess.PAWN: "♟", chess.ROOK: "♜", chess.KNIGHT: "♞",
    chess.BISHOP: "♝", chess.QUEEN: "♛", chess.KING: "♚",
}

def styled_piece(piece):
    if not piece:
        return " "
    if piece.color == chess.WHITE:
        return f"[bold white]{WHITE_PIECES[piece.piece_type]}[/]"
    return f"[bold black]{BLACK_PIECES[piece.piece_type]}[/]"

class Square(Button):
    def __init__(self, square, light):
        super().__init__("")
        self.square = square
        self.light = light

    def update_piece(self, board):
        self.label = styled_piece(board.piece_at(self.square))
        self.styles.background = "#d2b48c" if self.light else "#8b5a2b"

class ChessTUI(App):
    CSS = """
    Grid { grid-size: 8; width: 48; height: 24; }
    Button { width: 6; height: 3; border: blank; }
    .selected { outline: thick blue; }
    """

    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.squares = {}
        self.selected = None

    def compose(self):
        yield Header()
        with Grid():
            for r in range(7, -1, -1):
                for f in range(8):
                    sq = chess.square(f, r)
                    btn = Square(sq, (r + f) % 2 == 0)
                    self.squares[sq] = btn
                    yield btn
        yield Footer()

    def on_mount(self):
        self.update_board()

    def update_board(self):
        for sq, btn in self.squares.items():
            btn.update_piece(self.board)

    async def on_button_pressed(self, event):
        sq = event.button.square

        if self.selected is None:
            if self.board.piece_at(sq) and self.board.color_at(sq) == self.board.turn:
                self.selected = sq
                event.button.add_class("selected")
            return

        move = chess.Move(self.selected, sq)
        self.clear_selection()

        if move in self.board.legal_moves:
            self.board.push(move)
            self.update_board()

    def clear_selection(self):
        for b in self.squares.values():
            b.remove_class("selected")
        self.selected = None


# =========================================================
# DASHBOARD / LAUNCHER
# =========================================================

class TermiChess(App):

    CSS = """
    #style { display: none; }
    """

    def compose(self):
        yield Header()
        with Center():
            with Vertical():
                yield Static("TermiChess", id="title")
                yield Select([("TUI", "ui"), ("CMD", "text")], prompt="Interface", id="iface")
                yield Select([("Solid", "0"), ("Color", "1")], prompt="Style", id="style")
                yield Button("Start", id="start")
        yield Footer()

    def on_select_changed(self, event):
        if event.select.id == "iface":
            self.query_one("#style").display = (event.value == "text")
            self.interface = event.value
        elif event.select.id == "style":
            self.style = event.value

    def on_button_pressed(self, event):
        if event.button.id == "start":
            self.exit()
            if self.interface == "text":
                run_cmd_game(self.style)
            else:
                ChessTUI().run()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    TermiChess().run()
