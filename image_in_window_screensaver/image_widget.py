from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QSizePolicy
from PySide2.QtGui import QPixmap, QMouseEvent
from PySide2.QtCore import Qt, QSize
import sys
import time
import random
import file_walker
from typing import List
from send2trash import send2trash
import custom_log as l
import bad_practise_global as bpg


class ImageWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self._layout = QHBoxLayout()
        self._image_label = QLabel()
        self._size_method = None
        self._seed = time.time()
        self._line_edit: QLineEdit = None
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        # self.sizeHint()
        random.seed(self._seed)

        # self._all_images: List = file_walker.walk(sys.argv[1])
        self._all_images: List = file_walker.walk()
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
        # self._all_images: List = file_walker.walk(sys.argv[1])
        self._all_images: List = file_walker.walk()
        self.image_shuffle()

    def _set_image(self, index):
        if index > len(self._all_images)-1:
            print("Oops")
            self.image_shuffle()
        l.log("setting image")
        image_pix_map = QPixmap(self._all_images[index])
        print("image: ", image_pix_map.width(), image_pix_map.height())

        # image_pix_map = image_pix_map.scaled(900, 900, Qt.KeepAspectRatio)
        # print(self.width(), self.height())
        window_height = bpg._window_height
        window_width = bpg._window_width
        print("window_size At set_image: ", window_width, window_height)
        if image_pix_map.width() < window_width and image_pix_map.height() < window_height:
            if image_pix_map.width() < bpg.screen_width and image_pix_map.height() < bpg.screen_height:
                print("image size is smaller than window in all ways.")
            else:
                image_pix_map = image_pix_map.scaled(
                    bpg.screen_width - bpg.width_spacing, bpg.screen_height - bpg.height_spacing, Qt.KeepAspectRatio)
        else:
            print("image size {} won't fit in window {}, {}, scaling".format(
                image_pix_map.size(), window_width, window_height))
            image_pix_map = image_pix_map.scaled(
                window_width - bpg.width_spacing, window_height - bpg.height_spacing, Qt.KeepAspectRatio)
            # window_ratio = window_width/window_height
            # image_ratio = image_pix_map.width()/image_pix_map.height()
            # print("ratios: ", window_ratio, image_ratio)
            # if window_ratio < 1:
            #     l.log("potrait mode")
            #     image_pix_map = image_pix_map.scaledToHeight(window_height-200, Qt.FastTransformation)
            # else:
            #     l.log("landscape mode")
            #     image_pix_map = image_pix_map.scaledToWidth(window_width-90, Qt.FastTransformation)
            # quit()
            # image_pix_map = image_pix_map.scaledToWidth(window_width-50, Qt.FastTransformation)
        print("image: ", image_pix_map.width(), image_pix_map.height())

        #
        self._image_label.setPixmap(image_pix_map)
        if self._line_edit:
            self._line_edit.setText(self._all_images[index])

    def set_line_edit(self, edit_line: QLineEdit):
        self._line_edit = edit_line

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.image_next()
        elif event.button() == Qt.MouseButton.RightButton:
            self.image_previous()

    def get_current_image_path_str(self) -> str:
        return self._all_images[self._current_index]
