import os

from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QSizePolicy, QVBoxLayout
from PySide2.QtGui import QPixmap, QMouseEvent, QKeyEvent, QDesktopServices
from PySide2.QtCore import Qt, QSize, Slot, QUrl
import time
import random
import file_walker
from typing import List
from send2trash import send2trash
import custom_log as l
import bad_practise_global as bpg


class ImageWidget(QWidget):
    def __init__(self):
        self.default_title = "Amit's Image Viewer"
        QWidget.__init__(self)
        self._layout = QVBoxLayout()
        self._image_label = QLabel(self)
        self._image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._image_label.setScaledContents(True)
        self.is_full_screen: bool = False
        self._seed = time.time()
       
        random.seed(self._seed)

        # self._all_images: List = file_walker.walk(sys.argv[1])

        # self._set_image(self._current_index)
        self._layout.addWidget(self._image_label)
        self.setLayout(self._layout)
        self.initialize_images()

    def initialize_images(self, mode=None, current_image_path = None):
        self._all_images: List = file_walker.walk(mode)
        self._current_index = 0
        if current_image_path:
            self._current_index = self.get_index_from_image_path(current_image_path)
        # self.image_shuffle()
        self._set_image(self._current_index)

    

    def is_image_landscape(self, image: QPixmap):
        if image.width()/image.height() > 1:
            return True
        else:
            return False

    def get_index_from_image_path(self, image_path: str):
        # for i in range(0, len(self._all_images)):
        #     if self._all_images[i] is image_path:
        #         return i
        return self._all_images.index(image_path)

    def image_shuffle(self):
        l.log("shuffle")
        image_path = self._all_images[self._current_index]
        self._seed = time.time()
        random.seed(self._seed)
        random.shuffle(self._all_images)
        self._current_index = self.get_index_from_image_path(image_path)
        self._set_image(self._current_index)
       
        # self._current_index = 0
        # self._set_image(self._current_index)

    def revert_shuffle(self):
        l.log("revert shuffle")
        print(self._current_index)
        current_image_path = self._all_images[self._current_index]
        self.initialize_images(file_walker.get_mode(), current_image_path)
        
    def image_next(self):
        l.log("next")
        self._current_index += 1
        if self._current_index > len(self._all_images):
            self._current_index = 0
        self._set_image(self._current_index)
        # self.setFocus()

    def image_previous(self):
        l.log("previous")
        self._current_index -= 1
        if self._current_index <= -1*len(self._all_images):
            self._current_index = 0
        self._set_image(self._current_index)

    def image_delete(self):
        l.log("delete: " + self._all_images[self._current_index])
        send2trash(self._all_images[self._current_index])
        self._all_images.remove(self._all_images[self._current_index])
        self._set_image(self._current_index)

    def _set_image(self, index):
        if index > len(self._all_images)-1 or index < -1*len(self._all_images):
            l.log("error: shuffling again")
            index = 0
        self._current_index = index
        l.log("setting image")
        image_pix_map = QPixmap(self._all_images[self._current_index])
        print("image: ", image_pix_map.width(), image_pix_map.height())
        self._image_label.setPixmap(image_pix_map)
        self.set_title(self._all_images[self._current_index])

    # def set_line_edit(self, edit_line: QLineEdit):
    #     self._line_edit = edit_line

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.image_next()
        elif event.button() == Qt.MouseButton.RightButton:
            self.image_previous()

    @Slot()
    def _browse_event(self):
        print(os.path.dirname(self.get_current_image_path_str()))
        arguments: str = os.path.dirname(
            self.get_current_image_path_str())
        url_path = QUrl.fromLocalFile(arguments)
        print(url_path)
        QDesktopServices.openUrl(url_path)

    def set_title(self, image_path):
        new_title = self.default_title + image_path
        l.log("setting title: "+new_title)
        self.setWindowTitle(new_title)


    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        l.log("Key event at top_level_widget: " + str(key))
        if key == Qt.Key_S:
            l.log("Key S")
            self.image_shuffle()
        elif key == Qt.Key_Left or key == Qt.Key_Backspace or key == Qt.Key_P:
            l.log("Key left or backspace")
            self.image_previous()
        elif key == Qt.Key_Right or key == Qt.Key_N or key == Qt.Key_Space:
            l.log("Key Right / N / Space")
            self.image_next()
        elif key == Qt.Key_Delete:
            l.log("Key Delete")
            self.image_delete()
        elif key == Qt.Key_F:
            l.log("Key F")
            if self.is_full_screen:
                self.showNormal()
            else:
                self.showFullScreen()
            # toggle
            self.is_full_screen = not self.is_full_screen
        elif key == Qt.Key_B:
            l.log("Key B")
            self._browse_event()
        elif key == Qt.Key_1 or key == Qt.Key_L:
            l.log("Key 1 / L --> landscape mode")
            self.initialize_images("landscape/")
        elif key == Qt.Key_2 or key == Qt.Key_P:
            l.log("Key 2 / P --> Portrait mode")
            self.initialize_images("portrait/")
        elif key == Qt.Key_R:
            self.revert_shuffle()
        elif key == Qt.Key_3:
            l.log("Key 3 / Reset all")
            self.initialize_images()
        
        self.setFocus()
        # self.set_title(self.get_current_image_path_str())

    def get_current_image_path_str(self) -> str:
        return self._all_images[self._current_index]
