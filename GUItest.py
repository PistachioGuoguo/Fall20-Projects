import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
import reversi

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


class Reversi(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # load chessboard as background
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('img/chessboard.png')))
        self.setPalette(palette1)
        # load image for black and white pieces, and scale to 90% of GRID_SIZE
        self.black_piece = QPixmap('img/black_piece.png').scaledToWidth(PIECE_SIZE) # scale piece size to 90x90
        self.white_piece = QPixmap('img/biden_white_piece.png').scaledToWidth(PIECE_SIZE)

        # set window size and fix it
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setMaximumSize(QtCore.QSize(WINDOW_WIDTH, WINDOW_HEIGHT))

        # set window name and icon
        self.setWindowTitle("Pistachio-Guoguo's Othello")  # 窗口名称
        self.setWindowIcon(QIcon('img/pistachio.png'))  # 窗口图标

        # self.pieces = [QLabel(self) for i in range(64)]

        board = reversi.board
        self.draw_board(board)

        # self.draw_piece(0,0,WHITE)
        # self.draw_piece(1,0,BLACK)
        # self.draw_piece(5,7,WHITE)
        # self.draw_piece(3,4,BLACK)
        self.show()

    def draw_piece(self, x, y, color) :
        """
        Draw an assigned-color piece on screen, with indices in 2-D array
        """
        px, py = coord_to_pixel(x,y)
        new_piece = QLabel(self) # new object
        if color == BLACK:
            new_piece.setPixmap(self.black_piece)
        elif color == WHITE:
            new_piece.setPixmap(self.white_piece)
        new_piece.setGeometry(px, py, PIECE_SIZE, PIECE_SIZE)

    def draw_board(self, board):
        # draw pieces on an entire board
        h, w = board.shape
        for i in range(h):
            for j in range(w):
                self.draw_piece(i,j, board[i,j])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Reversi()
    sys.exit(app.exec_())
