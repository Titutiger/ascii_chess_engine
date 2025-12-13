import curses
import sys


class ChessBoard:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board = [
            ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
            ['♟'] * 8, ['.'] * 8, ['.'] * 8, ['.'] * 8, ['.'] * 8,
            ['♙'] * 8,
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        ]
        self.selected = None
        self.colors = {
            'dark': 1,
            'light': 2,
            'selected': 3
        }
        self.setup_colors()
        self.square_width = 3
        self.square_height = 1

    def setup_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # dark
        curses.init_pair(2, curses.COLOR_BLACK, -1)  # light (yellowish)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # selected

    def draw_board(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        for row in range(8):
            # Rank label
            self.stdscr.addstr(row * 2, 1, f"{8 - row}", curses.A_BOLD)

            for col in range(8):
                piece = self.board[row][col]
                x = col * self.square_width + 4
                y = row * self.square_height * 2

                if self.selected == (row, col):
                    color = self.colors['selected']
                elif (row + col) % 2 == 0:
                    color = self.colors['dark']
                else:
                    color = self.colors['light']

                self.stdscr.attron(curses.color_pair(color) | curses.A_BOLD)
                self.stdscr.addstr(y, x, piece)
                self.stdscr.attroff(curses.color_pair(color) | curses.A_BOLD)

            # Right rank label
            self.stdscr.addstr(row * 2, 26, f"{8 - row}", curses.A_BOLD)

        # File labels
        files = " a b c d e f g h "
        self.stdscr.addstr(16, 4, files, curses.A_BOLD)

        self.stdscr.refresh()

    def handle_mouse(self, m_event):
        _, mx, my, _, _ = m_event
        col = mx // self.square_width - 1
        row = my // 2

        if 0 <= row < 8 and 0 <= col < 8:
            pos = (row, col)
            if self.selected is None and self.board[row][col] != '.':
                self.selected = pos
            elif self.selected:
                fr, to = self.selected, pos
                target = self.board[to[0]][to[1]]
                if target == '.' or target in '♜♞♝♛♚':
                    self.board[to[0]][to[1]] = self.board[fr[0]][fr[1]]
                    self.board[fr[0]][fr[1]] = '.'
                self.selected = None
            self.draw_board()


def main(stdscr):
    curses.mouseinterval(1)
    curses.mousemask(curses.BUTTON1_CLICKED)

    board = ChessBoard(stdscr)
    board.draw_board()

    while True:
        try:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                _, m_event = curses.getmouse()
                board.handle_mouse(m_event)
            elif key == ord('q'):
                break
        except KeyboardInterrupt:
            break

    stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
