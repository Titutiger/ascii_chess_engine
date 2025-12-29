from textual.widget import Widget
from textual.widgets import Static
from textual.app import App, ComposeResult

class Spacer(Widget):
    def __init__(self):
        super().__init__()
        self.styles.width = "1fr" # Takes up available fractional space

class HorizontalBar(Static):
    def compose(self) -> ComposeResult:
        yield Static("Left", classes="item")
        yield Spacer() # Takes space between Left and Right
        yield Static("Right", classes="item")

    def on_mount(self):
        self.styles.layout = "horizontal" # Arrange children horizontally
        self.styles.height = 1
        self.query_class("item").styles.background = "blue"
        self.query_class("item").styles.width = "auto"

if __name__ == "__main__":
    app =
    app.run()