#!/usr/bin/python3
import os


from PIL import Image

from PyQt5.QtWidgets import (
    QGraphicsScene, QMainWindow, QFileDialog, QApplication)
from PyQt5.QtGui import QPixmap
import sys
import gui_window

from library import convert_util
from library import image_handler
from library import file_handler


class Image_Note(QMainWindow, gui_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Image_Note, self).__init__(parent)
        self.setupUi(self)
        self.button_browse.clicked.connect(self.browse_file)
        self.button_browse_pdf.clicked.connect(self.browse_pdf_file)

        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(40)
        self.button_reset.clicked.connect(self.reset)
        self.slider.valueChanged.connect(self.sensitivity_slider)
        self.button_delete.clicked.connect(self.remove_residual_images)
        self.button_save.clicked.connect(self.save_image)
        self.button_pdf_save.clicked.connect(self.save_pdf)
        self.visibility_widgets()

    def visibility_widgets(self,
                           disable: bool = False):
        self.all_widgets = [self.button_delete,
                            self.button_pdf_save, self.button_reset,
                            self.button_save, self.slider]

        for widget in self.all_widgets:
            widget.setEnabled(disable)
            print(type(widget))

    def sensitivity_slider(self):
        value = self.slider.value()
        print(value)
        self.thumbnail_image = Image.open(self.thumbnail_address)
        self.thumbnail_address_converted = \
            file_handler.filepath_modified_suffix(
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

    def save_pdf(self):
        import os
        if not os.path.exists(self.modified_image_address):
            self.save_image()
        convert_util.convert_image_to_pdf(
            self.modified_image_address,
            file_handler.change_path_extension(
                self.modified_image_address, ".pdf"))

    # def pdf_convert(self):
    #     self.save_image()
    #     convert_util.convert_image_to_pdf(self.modified_image_address,
    #                                       file_handler.change_path_extension(  # noqa
    #                                           self.modified_image_address,
    #                                           ".pdf"))

    def browse_pdf_file(self):
        self.pdf_file_address = QFileDialog.getOpenFileName(
            self, 'Open PDF File')
        self.file_address = file_handler.change_path_extension(
            self.pdf_file_address, ".png")
        convert_util.convert_pdf_to_image(
            self.pdf_file_address, self.file_address)
        self.process_file()

    def browse_file(self):

        response = QFileDialog.getOpenFileName(self, 'Open Image File')
        self.file_address = response[0]
        if not os.path.exists(self.file_address):
            return
        # return
        self.process_file()

    def process_file(self):
        self.thumbnail_address: str = file_handler.filepath_modified_suffix(
            self.file_address, "_thumbnail")
        self.modified_image_address: str = \
            file_handler.filepath_modified_suffix(
                self.file_address)
        image_handler.save_thumbnail(Image.open(
            self.file_address), self.thumbnail_address)
        self.visibility_widgets(True)
        self.load_graphics_image(self.thumbnail_address)

    def load_graphics_image(self, image_address: str):
        self.graphics_scene = QGraphicsScene()
        self.graphics_scene.addPixmap(QPixmap(image_address))
        self.graphicsView.setScene(self.graphics_scene)


def main():
    app = QApplication(sys.argv)
    form = Image_Note()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()
