import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
import reversi
import time

BLACK = 1
WHITE = 2

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
GRID_SIZE = 100
PIECE_SIZE = 0.9 * GRID_SIZE  # 90
GAP = (GRID_SIZE - PIECE_SIZE)/2 # 5

def coord_to_pixel(x,y):
    # convert from 2-D array index to pixel on QWidget
    # a[0,0] -> (5,5); a[1,0] -> (5, 105)
    return (GAP-1) + GRID_SIZE * y, (GAP-2) + GRID_SIZE * x # add minor shift to keep piece in center


def pixel_to_coord(x, y):
    # convert from pixel on QWidget to 2-D array coordinate
    return int( (x-(GAP-2)) / GRID_SIZE ), int( (y-(GAP-1)) // GRID_SIZE )


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()



    def init_UI(self):

        self.game = reversi.Game()

        # load chessboard as background
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('img/chessboard.png')))
        self.setPalette(palette1)

        # load image for black and white pieces, and scale to 90% of GRID_SIZE
        self.black_piece = QPixmap('img/black_piece.png').scaledToWidth(PIECE_SIZE) # scale piece size to 90x90
        self.white_piece = QPixmap('img/white_piece.png').scaledToWidth(PIECE_SIZE)

        # set each piece value to BLACK OR WHITE, else if draw new piece every time, the shade will overlay
        self.pieces = [QLabel(self) for i in range(64)]
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变

        # set window size and fix it
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setMaximumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))

        # set window name and icon
        self.setWindowTitle("Pistachio-Guoguo's Othello")  # 窗口名称
        self.setWindowIcon(QIcon('img/pistachio.png'))  # 窗口图标



        # rewrite the main_flow, replace visualization and input in GUI

        self.setMouseTracking(True)
        self.draw_board()
        self.show()

    def mousePressEvent(self, e):  # 玩家下棋
        if e.button() == Qt.LeftButton:
            x, y = e.x(), e.y()  # 鼠标坐标
            j, i = pixel_to_coord(x, y)  # 对应棋盘坐标
            if self.game.is_valid_move(i,j):
                self.game.take_move(i, j)
                self.draw_board()
                self.game.switch_turn() # let white player move (AI)

                # AI move
                ai_move = self.game.random_move()
                if ai_move:
                    self.game.take_move(ai_move[0],ai_move[1])
                    self.draw_board()
                self.game.switch_turn()




    def draw_piece(self, x, y, color) :
        """
        Format: self.draw_piece(5,3,BLACK)
        Draw an assigned-color piece on screen, with indices in 2-D array
        """
        if color == BLACK:
            self.pieces[x * 8 + y].setPixmap(self.black_piece)
        elif color == WHITE:
            self.pieces[x * 8 + y].setPixmap(self.white_piece)
        px, py = coord_to_pixel(x, y)
        self.pieces[x * 8 + y].setGeometry(px, py, PIECE_SIZE, PIECE_SIZE)

    def draw_board(self):
        # draw pieces on an entire board
        h, w = self.game.board.shape
        for i in range(h):
            for j in range(w):
                self.draw_piece(i,j, self.game.board[i,j])





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())

