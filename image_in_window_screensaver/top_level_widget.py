from PySide2.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                               QHBoxLayout)
from image_widget import ImageWidget
from PySide2.QtCore import Qt, QUrl
from PySide2.QtCore import Slot
from PySide2.QtGui import QKeyEvent, QDesktopServices
import custom_log as l
import os


class TopLevelWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # set widget layout - vertical
        # self._layout = QVBoxLayout()

        # create top horizontal bar of buttons
        self._top:QHBoxLayout = QHBoxLayout()
        self.setFixedHeight(50)


        self._button_previous = QPushButton("Previous")
        self._button_next = QPushButton("Next")
        self._button_shuffle = QPushButton("Shuffle")
        self._button_play = QPushButton("Play")
        self._button_delete = QPushButton("Delete")
        self._button_browse = QPushButton("Browse")

        # add buttons to top layout
        self._top.addWidget(self._button_shuffle)
        self._top.addWidget(self._button_previous)
        self._top.addWidget(self._button_next)
        # self._top.addWidget(self._button_play)
        self._top.addWidget(self._button_browse)
        self._top.addWidget(self._button_delete)

        # self._layout.addLayout(self._top)
        self.setLayout(self._top)
        self._image_widget_connector: ImageWidget = None

        self._button_shuffle.clicked.connect(self._shuffle_event)
        self._button_previous.clicked.connect(self._previous_event)
        self._button_next.clicked.connect(self._next_event)
        self._button_delete.clicked.connect(self._delete_event)
        self._button_browse.clicked.connect(self._browse_event)

    def connect_image_widget(self, image_widget: ImageWidget):
        self._image_widget_connector: ImageWidget = image_widget

    @Slot()
    def _shuffle_event(self):
        self._image_widget_connector.image_shuffle()

    @Slot()
    def _previous_event(self):
        self._image_widget_connector.image_previous()

    @Slot()
    def _next_event(self):
        self._image_widget_connector.image_next()

    @Slot()
    def _delete_event(self):
        self._image_widget_connector.image_delete()

    @Slot()
    def _browse_event(self):
        print(os.path.dirname(self._image_widget_connector.get_current_image_path_str()))
        arguments: str = os.path.dirname(
            self._image_widget_connector.get_current_image_path_str())
        url_path = QUrl.fromLocalFile(arguments)
        print(url_path)
        QDesktopServices.openUrl(url_path)
        # process = QProcess()
        # process.startDetached(command, arguments)
        # process.waitForFinished(-1)

    def keyReleaseEvent(self, event: QKeyEvent):
        l.log("Key event at top_level_widget: " + str(event.key()))
        if event.key() == Qt.Key_S:
            l.log("Key S")
            self._image_widget_connector.image_shuffle()
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Backspace or event.key() == Qt.Key_P:
            l.log("Key left or backspace")
            self._image_widget_connector.image_previous()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_N or event.key() == Qt.Key_Space:
            l.log("Key Right / N / Space")
            self._image_widget_connector.image_next()
        elif event.key() == Qt.Key_Delete:
            l.log("Key Delete")
            self._image_widget_connector.image_delete()
        elif event.key() == Qt.Key_F:
            l.log("Key F")
            self.showFullScreen()
        elif event.key() == Qt.Key_B:
            l.log("Key B")
            self._browse_event()
        self.setFocus()
