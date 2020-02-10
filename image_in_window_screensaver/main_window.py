#!./venv/bin/python3
from PySide2.QtWidgets import (QMainWindow, QApplication, QSizePolicy)
from PySide2.QtGui import QResizeEvent
from PySide2.QtCore import QSize
import bad_practise_global as bpg
import custom_log as l
from main_level_widget import MainWidget


class MainWindow(QMainWindow):

    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Amit's Image Viewer")
        self.setCentralWidget(widget)
        self._is_full_screen: bool = True
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setMaximumSize(QSize(bpg.screen_width, bpg.screen_height))

    # def sizeHint(self) -> QSize:
    #     return QSize(1920, 1080)

    def resizeEvent(self, event: QResizeEvent):
        print("caught!", event.size())
        self.resize(event.size().width(), event.size().height())
        bpg._window_height = event.size().height()
        bpg._window_width = event.size().width()

    # def toggle_full_screen(self):
    #     if self._is_full_screen:
    #         window.resize(900,900)
    #         self._is_full_screen = False
    #     else:
    #         window.resize(1920,1080)
    #         self._is_full_screen = True


if __name__ == '__main__':
    l.disable()
    import sys

    app = QApplication(sys.argv)
    widget = MainWidget()
    # widget = TopLevelWidget()
    # size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    # widget.setSizePolicy(size_policy)
    # widget.setFixedHeight(50)
    window = MainWindow(widget)
    window.show()
    window.resize(bpg.screen_width, bpg.screen_height)
    sys.exit(app.exec_())
