from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Grid, Horizontal
import chess
import sys

'''
WHITE_PIECES = {
    chess.PAWN: "♙",
    chess.ROOK: "♖",
    chess.KNIGHT: "♘",
    chess.BISHOP: "♗",
    chess.QUEEN: "♕",
    chess.KING: "♔",
}

BLACK_PIECES = {
    chess.PAWN: "♟",
    chess.ROOK: "♜",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}


def styled_piece(piece: chess.Piece | None) -> str:
    if not piece:
        return " "

    if piece.color == chess.WHITE:
        return f"[bold white]{WHITE_PIECES[piece.piece_type]}[/]"
    else:
        return f"[bold black]{BLACK_PIECES[piece.piece_type]}[/]"

'''

# ASCII fallback pieces
ASCII_WHITE = {
    chess.PAWN: "P",
    chess.ROOK: "R",
    chess.KNIGHT: "N",
    chess.BISHOP: "B",
    chess.QUEEN: "Q",
    chess.KING: "K",
}

ASCII_BLACK = {
    chess.PAWN: "p",
    chess.ROOK: "r",
    chess.KNIGHT: "n",
    chess.BISHOP: "b",
    chess.QUEEN: "q",
    chess.KING: "k",
}

# Unicode chess pieces
UNICODE_WHITE = {
    chess.PAWN: "♙",
    chess.ROOK: "♖",
    chess.KNIGHT: "♘",
    chess.BISHOP: "♗",
    chess.QUEEN: "♕",
    chess.KING: "♔",
}

UNICODE_BLACK = {
    chess.PAWN: "♟",
    chess.ROOK: "♜",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}

# Detect if terminal supports Unicode chess symbols
def unicode_supported() -> bool:
    try:
        # Try printing a chess symbol to stdout
        "♔".encode(sys.stdout.encoding)
        return True
    except Exception:
        return False

USE_UNICODE = unicode_supported()

WHITE_PIECES = UNICODE_WHITE if USE_UNICODE else ASCII_WHITE
BLACK_PIECES = UNICODE_BLACK if USE_UNICODE else ASCII_BLACK

def styled_piece(piece: chess.Piece | None) -> str:
    if not piece:
        return " "
    if piece.color == chess.WHITE:
        return f"[bold white]{WHITE_PIECES[piece.piece_type]}[/]"
    else:
        return f"[bold black]{BLACK_PIECES[piece.piece_type]}[/]"



class Square(Button):
    def __init__(self, square: chess.Square, is_light: bool):
        super().__init__("", id=f"sq-{square}")
        self.square = square
        self.is_light = is_light

    def set_piece(self, board: chess.Board):
        self.label = styled_piece(board.piece_at(self.square))

        # Board square coloring
        self.styles.background = "#d2b48c" if self.is_light else "#8b5a2b"


class ChessApp(App):
    CSS = """
    Grid {
        grid-size: 8;
        width: 48;
        height: 24;
    }

    Button {
        width: 6;
        height: 3;
        padding: 0;
        text-align: center;
        border: blank;
    }

    .selected {
        outline: thick blue;
    }

    #turn-indicator {
        width: 26;
        content-align: center middle;
    }
    """

    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.squares: dict[int, Square] = {}
        self.selected_square: int | None = None
        self.blink = True
        self.game_over = False
        self.game_over_reason = ""

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with Grid():
                for rank in range(7, -1, -1):
                    for file in range(8):
                        sq = chess.square(file, rank)
                        is_light = (rank + file) % 2 == 0
                        btn = Square(sq, is_light)
                        self.squares[sq] = btn
                        yield btn

            yield Static("", id="turn-indicator")

        yield Footer()

    def on_mount(self) -> None:
        self.refresh_board()
        self.update_turn_indicator()
        self.set_interval(0.6, self.blink_turn)

    def refresh_board(self) -> None:
        for btn in self.squares.values():
            btn.set_piece(self.board)

    def update_turn_indicator(self):
        indicator = self.query_one("#turn-indicator")

        if self.game_over:
            indicator.update(f"[bold red]{self.game_over_reason}[/]")
            return

        if self.board.turn == chess.WHITE:
            text = "[bold blink white]WHITE TO MOVE[/]"
        else:
            text = "[bold blink black on white]BLACK TO MOVE[/]"

        indicator.update(text if self.blink else "")

    def blink_turn(self):
        self.blink = not self.blink
        self.update_turn_indicator()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.game_over:
            return

        square = event.button.square

        if self.selected_square is None:
            if (
                self.board.piece_at(square)
                and self.board.color_at(square) == self.board.turn
            ):
                self.selected_square = square
                event.button.add_class("selected")
            return

        move = chess.Move(self.selected_square, square)
        self.clear_selection()

        if move in self.board.legal_moves:
            self.board.push(move)
            self.refresh_board()
            self.check_game_state()
            self.update_turn_indicator()

    def clear_selection(self):
        for btn in self.squares.values():
            btn.remove_class("selected")
        self.selected_square = None

    def check_game_state(self):
        if self.board.is_checkmate():
            winner = "White" if not self.board.turn else "Black"
            self.end_game(f"CHECKMATE — {winner} wins")

        elif self.board.is_stalemate():
            self.end_game("STALEMATE — Draw")

        elif self.board.is_insufficient_material():
            self.end_game("DRAW — Insufficient material")

    def end_game(self, reason: str):
        self.game_over = True
        self.game_over_reason = reason
        self.notify(
            reason,
            severity="error" if "CHECKMATE" in reason else "warning",
            timeout=6,
        )


if __name__ == "__main__":
    ChessApp().run()

