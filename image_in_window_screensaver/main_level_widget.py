from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit

from image_widget import ImageWidget
from top_level_widget import TopLevelWidget


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()

        # top bar widget
        self.top = TopLevelWidget()
        self.top.setFixedHeight(50)

        # image widget
        self.image = ImageWidget()

        # text widget
        self._line_edit = QLineEdit("TEXT HERE")
        
        # add widgets to layout
        self.layout.addWidget(self.top)
        self.layout.addWidget(self.image)
        self.layout.addWidget(self._line_edit)

        # add connectors to external widgets
        self.top.connect_image_widget(self.image)
        self.image.set_line_edit(self._line_edit)

        self.setLayout(self.layout)
