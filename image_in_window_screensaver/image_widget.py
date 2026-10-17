import os
import random
import time
from typing import List

from qtpy.QtCore import Qt, Slot, QUrl, QTimer
from qtpy.QtGui import QPixmap, QMouseEvent, QKeyEvent, QDesktopServices, \
    QKeySequence
from qtpy.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from send2trash import send2trash
import argument_handler as argh
import bad_practise_global as bpg
import custom_log as l
import file_walker


# Hand-maintained; keep in sync with the Shortcuts table in readme.md.
KEYMAP_HELP = """\
s                      shuffle images in list
Left / Backspace       previous image
Right / Space / n      next image
<  (shift+,)           previous 10th image
>  (shift+.)           next 10th image
Delete                 send current image to Trash

f                      toggle full screen mode
v                      view image in file browser
b                      bookmark current image
0                      go to bookmarked image (or where the shuffle started)

1                      landscape images only
2                      portrait images only
3                      reset all
4                      go to the 1st image, in whatever applied sort
r                      reverse the current order
e                      sort by date (new to old)
d                      sort by date (old to new)

p                      toggle play/pause
t                      pomodoro mode, delay increased to 25 minutes
y                      fast mode, delay decreased to 1 second
=  /  -                increase / decrease delay by 1 second
+  /  _                increase / decrease delay by 10 seconds

?                      show this keymap
Esc                    hide this keymap"""


class ImageWidget(QWidget):
    def __init__(self):
        self.default_title = "Amit's Image Viewer"
        QWidget.__init__(self)
        self._layout = QVBoxLayout()
        self._image_label = QLabel(self)
        self._image_label.setSizePolicy(QSizePolicy.Ignored,
                                        QSizePolicy.Ignored)
        self._image_label.setAlignment(Qt.AlignCenter)
        self._original_pixmap = None

        # keymap overlay, hidden until ? is pressed
        self._help_overlay = QLabel(self)
        self._help_overlay.setText("<pre>" + KEYMAP_HELP + "</pre>")
        self._help_overlay.setAlignment(Qt.AlignCenter)
        self._help_overlay.setStyleSheet(
            "background-color: rgba(0, 0, 0, 190); color: white;"
            " font-size: 14px;")
        self._help_overlay.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._help_overlay.hide()

        # delay toast: shows the new slideshow delay briefly, bottom center
        self._delay_toast = QLabel(self)
        self._delay_toast.setAlignment(Qt.AlignCenter)
        self._delay_toast.setStyleSheet(
            "background-color: rgba(0, 0, 0, 170); color: white;"
            " font-size: 28px; padding: 10px 24px; border-radius: 8px;")
        self._delay_toast.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._delay_toast.hide()
        self._delay_toast_timer = QTimer()
        self._delay_toast_timer.setSingleShot(True)
        self._delay_toast_timer.setInterval(2000)
        self._delay_toast_timer.timeout.connect(self._delay_toast.hide)

        # images_list
        self._all_images: List = []

        # properties
        self._shuffle_start_index = 0
        self._bookmark_path: str = None  # set by b, read by 0
        self._current_index = 0
        self.is_full_screen: bool = False
        # self.is_playing: bool = False
        self.is_playing: bool = bpg.autoplay
        self._seed = time.time()

        # timer
        self.timer = QTimer()
        self.timer.setInterval(bpg.pause_secs * 1000)
        self.timer.timeout.connect(self.play_image_next)

        random.seed(self._seed)

        # self._all_images: List = file_walker.walk(sys.argv[1])

        # self._set_image(self._current_index)
        self._layout.addWidget(self._image_label)
        self.setLayout(self._layout)
        self.initialize_images()
        if bpg.shuffle_from_start:
            self.image_shuffle()
        self._set_start_image()

    def _set_start_image(self):
        self.start_image = argh.get_start_image_path()
        if self.start_image:
            l.log("setting start image: "+self.start_image)
            index = self.get_index_from_image_path(
                    self.start_image)
            self._set_image(index)
            self._current_index = index


    def initialize_images(self, mode=None, current_image_path=None,
                          to_sort: bool = False,
                          reverse_sort: bool = False):
        self._all_images: List = file_walker.walk(mode, is_sorted=to_sort,
                                                  reverse_sort=reverse_sort)
        self._current_index = 0
        self._shuffle_start_index = 0
        if current_image_path:
            self._current_index = self.get_index_from_image_path(
                current_image_path)
            self._shuffle_start_index = self._current_index
        self._set_image(self._current_index)

    def is_image_landscape(self, image: QPixmap):
        if image.width() / image.height() > 1:
            return True
        else:
            return False

    def get_index_from_image_path(self, image_path: str):
        # for i in range(0, len(self._all_images)):
        #     if self._all_images[i] is image_path:
        #         return i

        try:
            return self._all_images.index(image_path)
        except ValueError:
            l.log("requested image {} not found. returning 0.".format(image_path))
            return 0

    def image_shuffle(self):
        l.log("shuffle")
        image_path = self._all_images[self._current_index]
        self._seed = time.time()
        random.seed(self._seed)
        random.shuffle(self._all_images)
        self._current_index = self.get_index_from_image_path(image_path)
        self._set_image(self._current_index)
        self._shuffle_start_index = self._current_index

        # self._current_index = 0
        # self._set_image(self._current_index)

    def reverse_sort(self):
        l.log("reversing current sort")
        print(self._current_index)
        current_image_path = self._all_images[self._current_index]
        self._all_images.reverse()
        self._current_index = self.get_index_from_image_path(current_image_path)


    def reset_all(self):
        """Reload every image from both folders, dropping any 1/2 filter.
        Reshuffles like 1/2 do, and lands on index 0 of the new list."""
        l.log("reset all: reloading unfiltered image list")
        self.initialize_images()
        if bpg.shuffle_from_start:
            self.image_shuffle()
            self._set_image(0)

    def sort_by_date(self, reverse_sort: bool = False):
        l.log("sorting images by date")
        print(self._current_index)
        current_image_path = self._all_images[self._current_index]
        self.initialize_images(mode=file_walker.get_mode(),
                               current_image_path=current_image_path,
                               to_sort=True,
                               reverse_sort=reverse_sort)

    def image_next(self, step: int = 1):
        l.log("next")
        self._current_index += step
        if self._current_index > len(self._all_images):
            self._current_index = 0
        self._set_image(self._current_index)
        # self.setFocus()

    def image_previous(self, step: int = 1):
        l.log("previous")
        self._current_index -= step
        if self._current_index <= -1 * len(self._all_images):
            self._current_index = 0
        self._set_image(self._current_index)

    def image_delete(self):
        l.log("delete: " + self._all_images[self._current_index])
        send2trash(self._all_images[self._current_index])
        self._all_images.remove(self._all_images[self._current_index])
        self._set_image(self._current_index)

    def _set_image(self, index):
        if index > len(self._all_images) - 1 or index < -1 * len(
                self._all_images):
            l.log("error: resetting again")
            index = 0
        self._current_index = index
        l.log("setting image")
        self._original_pixmap = QPixmap(self._all_images[self._current_index])
        print("image: ", self._original_pixmap.width(), self._original_pixmap.height())
        self._scale_and_display_image()
        self.set_title(self._all_images[self._current_index])

    def _scale_and_display_image(self):
        if self._original_pixmap and not self._original_pixmap.isNull():
            size = self._image_label.size()
            if size.width() <= 0 or size.height() <= 0:
                return

            if hasattr(self._original_pixmap, "scaledToFit"):
                scaled_pixmap = self._original_pixmap.scaledToFit(
                    size.width(), size.height())
            else:
                scaled_pixmap = self._original_pixmap.scaled(
                    size.width(),
                    size.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            self._image_label.setPixmap(scaled_pixmap)

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
        l.log("setting title: " + new_title)
        self.setWindowTitle(new_title)

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()

        l.log("Key event at top_level_widget: " + str(key) + " " + QKeySequence(
            key).toString() + "text: " +text)
        if key == Qt.Key_S:
            l.log("Key S")
            self.image_shuffle()
        elif key == Qt.Key_Left or key == Qt.Key_Backspace:
            l.log("Key left or backspace")
            self.image_previous()
        elif key == Qt.Key_Right or key == Qt.Key_N or key == Qt.Key_Space:
            l.log("Key Right / N / Space")
            self.image_next()
        elif key == Qt.Key_Greater:
            l.log("> pressed")
            self.image_next(10)
        elif key == Qt.Key_Less:
            l.log("< pressed")
            self.image_previous(10)
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
        elif key == Qt.Key_V:
            l.log("Key V")
            self._browse_event()
        elif key == Qt.Key_B:
            l.log("Key B / bookmark current image")
            self._bookmark_path = self.get_current_image_path_str()
        elif key == Qt.Key_1:
            l.log("Key 1 --> landscape mode")
            self.initialize_images("landscape/", current_image_path=self.start_image)
            if bpg.shuffle_from_start:
                self.image_shuffle()
        elif key == Qt.Key_2:
            l.log("Key 2 --> Portrait mode")
            self.initialize_images("portrait/", current_image_path=self.start_image)
            if bpg.shuffle_from_start:
                self.image_shuffle()
        elif key == Qt.Key_0:
            l.log("Key 0 --> go to bookmark")
            if self._bookmark_path:
                self._current_index = self.get_index_from_image_path(
                    self._bookmark_path)
            elif self._shuffle_start_index != 0:
                self._current_index = self._shuffle_start_index
            else:
                self._current_index = 0
            self._set_image(self._current_index)
        elif key == Qt.Key_R:
            self.reverse_sort()
        elif key == Qt.Key_D:
            self.sort_by_date()
        elif key == Qt.Key_E:
            self.sort_by_date(reverse_sort=True)
        elif key == Qt.Key_3:
            l.log("Key 3 / Reset all")
            self.reset_all()
        elif key == Qt.Key_4:
            l.log("Key 4 / Set image to 0th Index in whatever sort")
            self._set_image(index=0)
        elif key == Qt.Key_P:
            l.log("Key P / Play / Pause")
            self.toggle_play()
        # timer
        elif key == Qt.Key_Equal:
            l.log("equal pressed")
            self.increase_timer()
        elif key == Qt.Key_Plus:
            print("+ pressed")
            self.increase_timer(10)
        elif key == Qt.Key_Minus:
            print("dash pressed")
            self.decrease_timer()
        elif key == Qt.Key_Underscore:
            print("- pressed")
            self.decrease_timer(10)
        elif key == Qt.Key_Y:
            print("Y pressed")
            self.decrease_timer(bpg.max_pause_secs)
        elif key == Qt.Key_T:
            print("T pressed")
            self.increase_timer(bpg.max_pause_secs)
        elif key == Qt.Key_Question:
            l.log("? pressed / show keymap")
            self.show_help()
        elif key == Qt.Key_Escape:
            l.log("Esc pressed / hide keymap")
            self.hide_help()

        if self.is_playing:
            self.play()
        else:
            self.pause()

        self.setFocus()
        # self.set_title(self.get_current_image_path_str())

    def toggle_play(self):
        self.is_playing = not self.is_playing
        l.log(
            str.format(
                "toggle auto play from {} to {}",
                (str(self.is_playing)),
                (str(not self.is_playing)))
            )
        if self.is_playing:
            self.play()
            self.flash_toast("playing")
        else:
            self.pause()
            self.flash_toast("paused")

    def play(self):
        l.log("slideshow running")
        # self.is_playing = True
        self.timer.start()

    def pause(self):
        l.log("slideshow paused")
        # self.is_playing = False
        self.timer.stop()

    def play_image_next(self):
        if self.is_playing:
            l.log("play_image_next - auto_play: "
                  + str(self.is_playing)
                  + ", current_index: "
                  + str(self._current_index))
            self.image_next()
        else:
            l.log("stopping: auto_play: " + str(self.is_playing))
            self.timer.stop()

    def increase_timer(self, time=1):
        if (bpg.pause_secs + time) >= bpg.max_pause_secs:
            bpg.pause_secs = bpg.max_pause_secs
        else:
            bpg.pause_secs += time
        l.log("increasing pause_secs for autoplay: " + str(bpg.pause_secs))
        self.timer.setInterval(bpg.pause_secs * 1000)
        self.flash_delay()

    def decrease_timer(self, time=1):
        if (bpg.pause_secs - time) < bpg.least_pause_secs:
            # l.log(
            #     "ignoring decrease timer command as current value too low: " + str(
            #         bpg.pause_secs))
            bpg.pause_secs = bpg.least_pause_secs
        else:
            bpg.pause_secs -= time
        l.log("decreasing pause_secs for autoplay: " + str(bpg.pause_secs))
        self.timer.setInterval(bpg.pause_secs * 1000)
        self.flash_delay()

    def show_help(self):
        self._help_overlay.setGeometry(self.rect())
        self._help_overlay.raise_()
        self._help_overlay.show()

    def hide_help(self):
        self._help_overlay.hide()

    def flash_delay(self):
        self.flash_toast("{} s".format(bpg.pause_secs))

    def flash_toast(self, text: str):
        """Show text for 2 s at the bottom center. Repeated calls update the
        text and restart the countdown; only one toast ever exists."""
        self._delay_toast.setText(text)
        self._delay_toast.adjustSize()
        self._position_delay_toast()
        self._delay_toast.raise_()
        self._delay_toast.show()
        self._delay_toast_timer.start()

    def _position_delay_toast(self):
        size = self._delay_toast.size()
        x = (self.width() - size.width()) // 2
        y = self.height() - size.height() - 40
        self._delay_toast.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._scale_and_display_image()
        self._help_overlay.setGeometry(self.rect())
        self._position_delay_toast()

    def get_current_image_path_str(self) -> str:
        return self._all_images[self._current_index]
