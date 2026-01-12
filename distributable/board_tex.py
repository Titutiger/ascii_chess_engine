from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Grid
import chess


PIECE_SYMBOLS = {
    chess.PAWN: "♟",
    chess.ROOK: "♜",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}


class Square(Button):
    def __init__(self, square: chess.Square):
        super().__init__(" ", id=f"sq-{square}")
        self.square = square

    def set_piece(self, board: chess.Board):
        piece = board.piece_at(self.square)
        self.label = PIECE_SYMBOLS[piece.piece_type] if piece else " "



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
    }

    .selected {
        background: blue;
    }
    """

    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.squares: dict[int, Square] = {}
        self.selected_square: int | None = None

    def compose(self) -> ComposeResult:
        yield Header()

        with Grid():
            for rank in range(7, -1, -1):
                for file in range(8):
                    sq = chess.square(file, rank)
                    btn = Square(sq)
                    self.squares[sq] = btn
                    yield btn

        yield Footer()

    def on_mount(self) -> None:
        self.refresh_board()

    def refresh_board(self) -> None:
        for sq, btn in self.squares.items():
            btn.set_piece(self.board)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        square = event.button.square

        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.color_at(square) == self.board.turn:
                self.selected_square = square
                event.button.add_class("selected")
            return

        move = chess.Move(self.selected_square, square)
        self.clear_selection()

        if move in self.board.legal_moves:
            self.board.push(move)
            self.refresh_board()

    def clear_selection(self):
        for btn in self.squares.values():
            btn.remove_class("selected")
        self.selected_square = None


if __name__ == "__main__":
    app = ChessApp()
    app.run()
