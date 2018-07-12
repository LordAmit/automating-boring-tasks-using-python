#!/usr/bin/python3
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
from PIL import ImageQt
from PIL import ImageEnhance
from typing import List, Union

import sys
import gui_window

from library import convert_util
from library import image_handler
from library import file_handler


class Image_Note(QtGui.QMainWindow, gui_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Image_Note, self).__init__(parent)
        self.setupUi(self)
        self.button_browse.clicked.connect(self.browse_file)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(40)
        self.button_reset.clicked.connect(self.reset)
        self.slider.valueChanged.connect(self.sensitivity_slider)
        self.button_delete.clicked.connect(self.remove_residual_images)
        self.button_save.clicked.connect(self.save_image)

        self.visibility_widgets()

    def visibility_widgets(self,
                           disable: bool = False):
        self.all_widgets = [self.button_delete,
                            self.button_grayscale, self.button_reset,
                            self.button_save, self.slider]

        for widget in self.all_widgets:
            widget.setEnabled(disable)
            print(type(widget))

    def sensitivity_slider(self):
        value = self.slider.value()
        print(value)
        self.thumbnail_image = Image.open(self.thumbnail_address)
        self.thumbnail_address_converted = \
            file_handler.filepath_modified_prefix(
                self.thumbnail_address)
        convert_util.convert_sample(
            self.thumbnail_address, self.thumbnail_address_converted, value)
        self.load_graphics_image(self.thumbnail_address_converted)

    def reset(self):
        self.slider.setValue(40)
        self.thumbnail_image = Image.open(self.thumbnail_address)
        self.load_graphics_image(self.thumbnail_address)

    def remove_residual_images(self):
        file_handler.remove_file(self.thumbnail_address)
        file_handler.remove_file(self.thumbnail_address_converted)

    def save_image(self):
        value = self.slider.value()
        convert_util.convert_full_image(
            self.file_address, self.modified_image_address, value)
        # self.remove_residual_images()

    def grayscale_convert(self):
        pass

    def browse_file(self):
        self.file_address = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Image File')
        self.graphics_scene = QGraphicsScene()
        self.thumbnail_address: str = file_handler.filepath_modified_prefix(
            self.file_address, "thumbnail_")
        self.modified_image_address: str = \
            file_handler.filepath_modified_prefix(self.file_address)
        image_handler.save_thumbnail(Image.open(
            self.file_address), self.thumbnail_address)
        self.visibility_widgets(True)
        # pixmap = QPixmap(file_address).scaledToWidth(200)
        # pixmap.save("ssomething.jpg")
        # self.graphics_scene.addPixmap(QPixmap(self.thumbnail_address))
        # self.graphicsView.setScene(self.graphics_scene)
        # self.graphicsView.show()
        self.load_graphics_image(self.thumbnail_address)

    def load_graphics_image(self, image_address: str):
        self.graphics_scene.addPixmap(QPixmap(image_address))
        self.graphicsView.setScene(self.graphics_scene)


def main():
    app = QtGui.QApplication(sys.argv)
    form = Image_Note()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()
