import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QStatusBar, QCheckBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() # IMPORTANT!!!!! Windows are hidden by default.
    # Start the event loop.
    app.exec_()