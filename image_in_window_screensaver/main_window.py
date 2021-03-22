import os

from qtpy.QtWidgets import (QMainWindow, QApplication, QSizePolicy, QWidget)
from PySide2.QtGui import QResizeEvent, QKeyEvent, QDesktopServices
from PySide2.QtCore import QSize, Slot, QUrl
import bad_practise_global as bpg
import custom_log as l
from PySide2.QtCore import Qt
# from main_level_widget import MainWidget
from image_widget import ImageWidget

if __name__ == '__main__':
    # l.disable()
    import sys

    app = QApplication(sys.argv)
    image_widget = ImageWidget()
    image_widget.show()
    image_widget.resize(500, 500)
    # window.resize(bpg.screen_width, bpg.screen_height)
    sys.exit(app.exec_())
