from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
import sys
import time
import random
import file_walker
from typing import List
from send2trash import send2trash
import custom_log as l


class ImageWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self._layout = QHBoxLayout()
        self._image_label = QLabel()
        self._size_method = None
        self._seed = time.time()
        self._line_edit: QLineEdit = None
        random.seed(self._seed)

        self._all_images: List = file_walker.walk(sys.argv[1])
        self._current_index = 0
        self.image_shuffle()
        # self._set_image(self._current_index)
        self._layout.addWidget(self._image_label)
        self.setLayout(self._layout)

    def image_shuffle(self):
        l.log("shuffle")
        self._seed = time.time()
        random.seed(self._seed)
        random.shuffle(self._all_images)
        self._current_index = 0
        self._set_image(self._current_index)

    def image_next(self):
        l.log("next")
        self._current_index += 1
        self._set_image(self._current_index)
        # self.setFocus()

    def image_previous(self):
        l.log("previous")
        self._current_index -= 1
        self._set_image(self._current_index)

    def image_delete(self):
        l.log("delete: " + self._all_images[self._current_index])
        send2trash(self._all_images[self._current_index])
        self._all_images: List = file_walker.walk(sys.argv[1])
        self.image_shuffle()

    def _set_image(self, index):
        l.log("setting image")
        image_pix_map = QPixmap(self._all_images[index])

        # image_pix_map = image_pix_map.scaled(900, 900, Qt.KeepAspectRatio)
        image_pix_map = image_pix_map.scaled(self.width(), self.height() - 20, Qt.KeepAspectRatio)
        self._image_label.setPixmap(image_pix_map)
        if self._line_edit:
            self._line_edit.setText(self._all_images[index])

    def set_line_edit(self, edit_line: QLineEdit):
        self._line_edit = edit_line
