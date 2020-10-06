#!./venv/bin/python3
import os

from PySide2.QtWidgets import (QMainWindow, QApplication, QSizePolicy, QWidget)
from PySide2.QtGui import QResizeEvent, QKeyEvent, QDesktopServices
from PySide2.QtCore import QSize, Slot, QUrl
import bad_practise_global as bpg
import custom_log as l
from PySide2.QtCore import Qt
# from main_level_widget import MainWidget
from image_widget import ImageWidget


class MainWindow(QMainWindow):

    # def __init__(self, widget):
    #     QMainWindow.__init__(self)
    #     self.default_title = "Amit's Image Viewer"
    #     self.setWindowTitle(self.default_title)
    #     self.setCentralWidget(widget)
    #     self.layout()
    #     self._is_full_screen: bool = True
    #     self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    #     self.image_widget: QWidget = widget
    #     self.setMaximumSize(QSize(bpg.screen_width, bpg.screen_height))

    # def sizeHint(self) -> QSize:
    #     return QSize(1920, 1080)

    # def resizeEvent(self, event: QResizeEvent):
    #     print("resizing window!", event.size())
    #     print("resizing image_widget: ", self.image_widget.size())
    #     self.resize(event.size().width(), event.size().height())
    #     bpg._window_height = event.size().height()
    #     bpg._window_width = event.size().width()

    def set_title(self, image_path):
        new_title = self.default_title + image_path
        l.log("setting title: "+new_title)
        self.setWindowTitle(new_title)

    # def keyReleaseEvent(self, event: QKeyEvent):
    #     l.log("Key event at top_level_widget: " + str(event.key()))
    #     if event.key() == Qt.Key_S:
    #         l.log("Key S")
    #
    #         self.image_widget.image_shuffle()
    #     elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Backspace or event.key() == Qt.Key_P:
    #         l.log("Key left or backspace")
    #         self.image_widget.image_previous()
    #     elif event.key() == Qt.Key_Right or event.key() == Qt.Key_N or event.key() == Qt.Key_Space:
    #         l.log("Key Right / N / Space")
    #         self.image_widget.image_next()
    #     elif event.key() == Qt.Key_Delete:
    #         l.log("Key Delete")
    #         self.image_widget.image_delete()
    #     elif event.key() == Qt.Key_F:
    #         l.log("Key F")
    #         self.showFullScreen()
    #     elif event.key() == Qt.Key_B:
    #         l.log("Key B")
    #         self._browse_event()
    #     # self.setFocus()
    #     self.set_title(self.image_widget.get_current_image_path_str())
    #
    #
    # @Slot()
    # def _browse_event(self):
    #     print(os.path.dirname(self.image_widget.get_current_image_path_str()))
    #     arguments: str = os.path.dirname(
    #         self.image_widget.get_current_image_path_str())
    #     url_path = QUrl.fromLocalFile(arguments)
    #     print(url_path)
    #     QDesktopServices.openUrl(url_path)
    # def toggle_full_screen(self):
    #     if self._is_full_screen:
    #         window.resize(900,900)
    #         self._is_full_screen = False
    #     else:
    #         window.resize(1920,1080)
    #         self._is_full_screen = True


if __name__ == '__main__':
    # l.disable()
    import sys

    app = QApplication(sys.argv)
    # widget = MainWidget()
    # widget = TopLevelWidget()
    # size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    # widget.setSizePolicy(size_policy)
    # widget.setFixedHeight(50)
    image_widget = ImageWidget()

    # window = MainWindow(widget)
    # window = MainWindow(image_widget)
    # window.show()
    image_widget.show()
    image_widget.resize(500, 500)
    # window.resize(bpg.screen_width, bpg.screen_height)
    sys.exit(app.exec_())
