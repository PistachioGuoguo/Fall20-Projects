from GUI_test import OthelloWindow
from GUI_test import QApplication, sys, QPixmap, Qt, QPalette, QtGui, QLabel
from GUI_test import BLACK, WHITE, PIECE_SIZE, pixel_to_coord, coord_to_pixel
from kingOthello import KingOthello, BLACK_KING, WHITE_KING, get_board


class KingOthelloWindow(OthelloWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.game = KingOthello()
        OthelloWindow.load_background(self)
        self.load_piece_asset()
        self.draw_board()

    def load_piece_asset(self):
        self.black_king_piece = QPixmap('img/black_king_piece.png').scaledToWidth(PIECE_SIZE)  # scale piece size to 90x90
        self.white_king_piece = QPixmap('img/white_king_piece.png').scaledToWidth(PIECE_SIZE)
        OthelloWindow.load_piece_asset(self)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            x, y = e.x(), e.y()  # mouse position (pixels)
            j, i = pixel_to_coord(x, y)
            if self.game.is_valid_move(i,j):
                self.game.take_move(i, j)
                self.draw_board()
                self.game.switch_turn()

        if e.button() == Qt.RightButton: # right click means place a king
            x, y = e.x(), e.y()  # mouse position (pixels)
            j, i = pixel_to_coord(x, y)
            if self.game.is_valid_move(i, j, is_king=True):
                self.game.take_move(i, j, is_king=True)
                self.draw_board()
                self.game.switch_turn()


    def draw_piece(self, x, y, color):
        if color == BLACK:
            self.pieces[x * 8 + y].setPixmap(self.black_piece)
        elif color == WHITE:
            self.pieces[x * 8 + y].setPixmap(self.white_piece)
        elif color == BLACK_KING:
            self.pieces[x * 8 + y].setPixmap(self.black_king_piece)
        elif color == WHITE_KING:
            self.pieces[x * 8 + y].setPixmap(self.white_king_piece)
        px, py = coord_to_pixel(x, y)
        self.pieces[x * 8 + y].setGeometry(px, py, PIECE_SIZE, PIECE_SIZE)


    def draw_board(self):

        # draw all pieces
        h, w = self.game.board.shape
        for i in range(h):
            for j in range(w):
                self.draw_piece(i, j, self.game.board[i, j])

        # clear previous feasible move markers
        # for pos in self.feasibility:
        #     pos.clear()
        # feasible_moves = self.game.find_all_valid_moves()

        # mark new feasible moves
        # for move in feasible_moves:
        #     x, y = move[0], move[1]
        #     self.feasibility[x * 8 + y].setPixmap(self.feasible_move)
        #     px, py = coord_to_pixel(x, y)
        #     self.feasibility[x * 8 + y].setGeometry(px + .3 * PIECE_SIZE, py, PIECE_SIZE, PIECE_SIZE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KingOthelloWindow()
    window.show()
    sys.exit(app.exec_())