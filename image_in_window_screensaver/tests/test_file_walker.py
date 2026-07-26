import sys
from unittest import TestCase

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QApplication, QLabel

sys.argv = ["image_viewer", "--path", "/tmp"]

from image_widget import ImageWidget


class TestImageWidget(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_scale_and_display_image_handles_pixmap_scaling(self):
        widget = ImageWidget.__new__(ImageWidget)
        widget._image_label = QLabel()
        widget._image_label.resize(200, 100)
        widget._original_pixmap = QPixmap(400, 200)

        widget._scale_and_display_image()

        pixmap = widget._image_label.pixmap()
        self.assertIsNotNone(pixmap)
        self.assertFalse(pixmap.isNull())
