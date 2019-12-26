#!/usr/bin/python3

# from PyQt4 import QtGui
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *

import sys
from PySide2.QtWidgets import QMainWindow, QApplication

from gui import gui
from library import text_handler


class NoteExtractor(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(NoteExtractor, self).__init__(parent)
        self.setupUi(self)
        self.button_output. clicked.connect(self.output_function)
        self.button_markdown_output.clicked.connect(
            self.output_markdown_function)

    def output_function(self):
        content = self.getcontents()
        self.setcontents(text_handler.process_content(content))

    def output_markdown_function(self):
        content = self.getcontents()
        self.setcontents(text_handler.process_content(content, True))

    def getcontents(self) -> str:
        return self.textEdit_input.toPlainText()

    def setcontents(self, value: str) -> None:
        self.textedit_output.setText(value)


def main():
    app = QApplication(sys.argv)
    form = NoteExtractor()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
