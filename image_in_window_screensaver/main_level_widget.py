from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QSpacerItem
from PySide2.QtCore import Slot
from image_widget import ImageWidget
from top_level_widget import TopLevelWidget
import bad_practise_global

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()

        # top bar widget
        self.top = TopLevelWidget()
        # self.top.setFixedHeight(70)

        # self.spacer = QSpacerItem(w = bad_practise_global._window_width-100, h=1)

        # image widget
        self.image = ImageWidget()

        # text widget
        self._line_edit = QLineEdit("TEXT HERE")
        self._line_edit.setFixedHeight(20)

        # add widgets to layout
        self.layout.addWidget(self.top)
        self.layout.addStretch(1)
        # self.layout.insertSpacing(1, 1)
        self.layout.addWidget(self.image)
        self.layout.addStretch(1)
        self.layout.addWidget(self._line_edit)

        # add connectors to external widgets
        self.top.connect_image_widget(self.image)
        self.image.set_line_edit(self._line_edit)

        self.setLayout(self.layout)

