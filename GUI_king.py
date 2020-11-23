from GUI_normal import OthelloWindow
from GUI_normal import QApplication, sys, QPixmap, Qt, QPalette, QtGui, QLabel, QMessageBox
from GUI_normal import BLACK, WHITE, PIECE_SIZE, pixel_to_coord, coord_to_pixel
from minimax import KingOthello, BLACK_KING, WHITE_KING
from copy import deepcopy
import time


class KingOthelloWindow(OthelloWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()


    def init_UI(self): # override by redefining load_piece_asset
        self.game = KingOthello()
        OthelloWindow.load_background(self)
        self.load_piece_asset()
        self.setWindowTitle("Pistachio-Guoguo's King Othello")  # 窗口名称
        self.draw_board()


    def load_piece_asset(self): # override method by adding king piece assets
        self.black_king_piece = QPixmap('img/black_king_piece.png').scaledToWidth(PIECE_SIZE)  # scale piece size to 90x90
        self.white_king_piece = QPixmap('img/white_king_piece.png').scaledToWidth(PIECE_SIZE)
        OthelloWindow.load_piece_asset(self)


    def mousePressEvent(self, e):
        # left click is normal piece, right click is king piece
        if e.button() == Qt.LeftButton:
            x, y = e.x(), e.y()  # mouse position (pixels)
            j, i = pixel_to_coord(x, y)
            if self.game.is_valid_move(i,j):
                self.game.take_move(i, j)
                self.draw_board()
                self.check_and_AI_move()

        elif e.button() == Qt.RightButton: # try to place a king
            x, y = e.x(), e.y()
            j, i = pixel_to_coord(x, y)
            if self.game.is_valid_move(i, j, is_king=True):
                self.game.take_move(i, j, is_king=True)
                self.draw_board()
                self.check_and_AI_move()

    def check_and_AI_move(self):
        if self.game.is_game_end():  # check end-of-game after a move is taken
            self.game_over()
        else:
            self.game.switch_turn()  # let white player move (AI)
            # AI move
            ai_move = self.game.minimax_move()
            if ai_move:
                self.game.take_move(ai_move[0], ai_move[1], ai_move[2])
                self.game.switch_turn()  # hand over to Human, convenient to draw feasible moves
                self.draw_board()
                if not self.game.find_all_valid_moves(): # human player has no valid move
                    time.sleep(0.5)
                    print('No move for human.')
                    self.check_and_AI_move()
            else:
                print("No move for AI.")
                self.game.switch_turn()  # no moves, hand over to other player
            if self.game.is_game_end():  # no moves for both side
                self.game_over()


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
        for pos in self.feasibility:
            pos.clear()
        # self.feasibility = [QLabel(self) for i in range(64)]
        feasible_moves = self.game.find_all_valid_moves()

        # mark new feasible moves
        for move in feasible_moves:
            x, y = move[0], move[1]
            self.feasibility[x * 8 + y].setPixmap(self.feasible_move)
            px, py = coord_to_pixel(x, y)
            self.feasibility[x * 8 + y].setGeometry(px + .3 * PIECE_SIZE, py, PIECE_SIZE, PIECE_SIZE)

    def game_over(self):
        # a message box to restart or quit game
        msg = self.game.finish_count(return_option='summary').split('--')

        reply = QMessageBox.question(self, msg[2].strip(), msg[1] + 'Restart?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.game = KingOthello() # reset
            for piece in self.pieces:
                piece.clear()
            self.draw_board()
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KingOthelloWindow()
    window.show()
    sys.exit(app.exec_())