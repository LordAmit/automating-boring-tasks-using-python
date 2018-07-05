from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
from PIL import ImageQt
from PIL import ImageEnhance

import sys
import gui_window


class Image_Note(QtGui.QMainWindow, gui_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Image_Note, self).__init__(parent)
        self.setupUi(self)
        self.button_browse.clicked.connect(self.browse_file)

    def browse_file(self):
        file_address = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Image File')
        print(file_address)


def main():
    app = QtGui.QApplication(sys.argv)
    form = Image_Note()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()
