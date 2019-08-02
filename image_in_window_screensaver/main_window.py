from PySide2.QtWidgets import (QMainWindow, QApplication)
from main_level_widget import MainWidget
import custom_log as l

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Amit's Image Viewer")
        self.setCentralWidget(widget)
        self._is_full_screen: bool = True

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
    window.resize(1920, 1080)
    sys.exit(app.exec_())
